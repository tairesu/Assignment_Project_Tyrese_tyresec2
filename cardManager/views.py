#import stripe
import urllib.request
import json
from io import BytesIO
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, views as auth_views
from django.http import HttpResponse
from django.http.response import JsonResponse
# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, ListView, DetailView, RedirectView, TemplateView
from django.views.generic.base import ContextMixin, View
from django.template import loader
from django.db.models import Count, Q
from django.db.models.functions import TruncDay
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from cardManager.models import (
	Card,
	Profile,
	Owner,
	Usage,
	Design,
	Request
)
from .forms import (
	CardForm,
	ProfileForm,
	RequestForm,
)

# Home Page fbv
class HomePage(ListView):
    model = Design
    template_name = 'cardManager/home.html'
    

def order_create(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        owner = Owner.objects.get(pk=request.user.pk)
        if form.is_valid():
            #https://stackoverflow.com/questions/77784821/how-to-add-value-into-a-form-before-saving-in-django
            order_instance = form.save(commit=False)
            order_instance.owner = owner
            form.save()
        else: 
        	print(form.errors)
    
# Create and Saves Usage instance, given card field
def __add_to_usage(request, card):
	print('\ninit\'d __add_to_usage')
	new_use = Usage(card=card)
	new_use.save()


	# Handles redirects for a scanned card matching card_token 
def card_detail(request,card_token):
	card = get_object_or_404(Card, token=card_token)
	is_owned = not (card.owner == None)
	is_redirecting = not (card.reroute_url == "")

	if is_owned:
		__add_to_usage(request, card) 
		
	if is_owned and not card.show_profile and is_redirecting:
		return redirect(card.reroute_url)
	elif is_owned and card.show_profile:
		return redirect('profile_view', profile_slug=card.owner.profile.profile_slug)
	elif is_owned and not is_redirecting:
		return redirect('card_update_view',pk=card.pk)
	elif not is_owned:
		return redirect('card_activate_view', card_token=card_token)	


class CardDetail(DetailView):
	model = Card
	slug_field = 'token'
	slug_url_kwarg = 'card_token'
	template_name = 'cardManager/activate.html'

	def get(self,request, **kwargs):
		card = self.get_object()
		if card.owner:
			return redirect('card_view', card_token=card.token)
		return super().get(self, request, **kwargs)


class CardUpdate(UpdateView):
	model = Card
	form_class = CardForm
	slug_field = 'token'
	slug_url_kwarg = 'card_token'
	template_name = 'cardManager/card_update.html'
	success_url = reverse_lazy('dashboard_view')


def card_update(request, card_token):
	"""
		FBV for handling card update functionality
	"""
	card = get_object_or_404(Card, token=card_token)
	initial_alias = card.alias
	if request.method == "GET":
		# Populate form with data from card model instance
		form = CardForm(instance=card)
		hide_redirect_div = card.show_profile
	elif request.method == "POST":
		# Let's update the current card instance with data from forms 		
		form = CardForm(request.POST, instance=card)
		hide_redirect_div = (card.show_profile or request.POST.get('show_profile')) and "route" not in str(form.errors)
		if form.is_valid():
			submitted_alias = form.cleaned_data['alias']
			"""
			 A8: form.save() was being called when the alias wasn't unique
			 I'll handle the error gracefully by throwing an error when: 
				- The inital alias differs from the submitted alias
				- AND when the submitted alias and card.owner combo exists already  
			
			"""
			alias_has_changed = not submitted_alias == initial_alias
			alias_in_use = ( Card.objects.filter(alias=submitted_alias, owner=card.owner).exists() )
			if alias_in_use and alias_has_changed:
				form.add_error("alias", "A card already has this name")
			else:
				form.save()
				return redirect('dashboard_view')
			

	
	return render(request, 'cardManager/card_update.html', {'form': form, 'card': card, 'hide_redirect_div': hide_redirect_div})


# Render profile template using the slugs instead of pk
class ProfileDetail(DetailView):
	model = Profile
	template_name = 'cardManager/profile.html'
	slug_field = 'profile_slug'
	slug_url_kwarg = 'profile_slug'

class ProfileUpdate(UpdateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'cardManager/profile_update.html'
	slug_field = 'profile_slug'
	slug_url_kwarg = 'profile_slug'

# Renders dashboard template with owner cards
class UserDashboard(ContextMixin, View):
	template_name = 'cardManager/dashboard.html'

	def get(self, request, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.template_name, context)

	# I need to alter the context that goes to the dashboard template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		owner_id = self.request.user.pk
		owner_cards = Card.objects.filter(owner_id=owner_id)
		recent_activities = Usage.objects.filter(card__owner=owner_id).order_by('-date_used')[0:5]
		context['user_cards'] = owner_cards
		context['recent_activities'] = recent_activities
		return context


class Stats(ListView):
	model = Usage
	template_name = 'cardManager/stats.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		query = self.request.GET.get('query')
		card_results = None
		if query:
			card_results = (
				Card.objects
				.filter(
					Q(alias__icontains=query) |
					Q(token__icontains=query) | 
					Q(owner__first_name__icontains=query) |
					Q(owner__last_name__icontains=query) |
					Q(owner__email__startswith=query) 
				)
			)

		context['query'] = query
		context['card_results'] = card_results

		# Narrowed QuerySet containing Card instances that belong to someone 
		claimed_cards = Card.objects.exclude(owner=None)
		# Total number of cards that belong to someone
		context['n_cards_claimed'] = claimed_cards.count()

		# Total number of Usage model records
		context['n_taps'] = Usage.objects.exclude(card__owner=None).count()

		# Total number of card Owners
		context['n_users'] = Owner.objects.count()

		"""
		Card taps per owner:

		1) Start with all Usage objects.
		2) Exclude usages where the related card has no owner.
		3) Group the remaining usages by the card owner's ID.
		4) Annotate each group with a new field 'n_card_taps' 
			representing the number of Usage records (taps)
			associated with that owner's cards.
		"""
		user_taps = (
			Usage.objects
			.exclude(card__owner=None)
			.values('card__owner_id')
			.annotate(n_card_taps=Count('card'))
			.order_by('-n_card_taps')[0:3]
		) # ==> <QuerySet [{'card__owner_id': 1, 'n_card_taps': 37},{..}]>

		# Create a list that formats user_taps to include Owner instance (instead of the owner's ID)   
		cleaned_user_taps = [
			{
				# Use card__owner_id to retrieve Owner instance 
				'user': Owner.objects.get(pk=item['card__owner_id']),
				# Keep n_card_taps
				'n_card_taps': item['n_card_taps']
			} 
			for item in user_taps 
		] # ==> [{'user': <Owner: Tyrese Cook>, 'n_card_taps': 37}, {...}]
		context['user_taps'] = cleaned_user_taps

		""" 
		uses per design

		1) Start with claimed Card objects
		2) Group the remaining cards by the card design_id
		3) Annotate each unique design with a new field 'n_uses'
			which counts the nuber of Card records
			associated with a unique design
		4) Order data by n_uses
		"""
		design_usage = (
			claimed_cards.values('design_id')
			.annotate(n_uses=Count('design'))
			.order_by('-n_uses') # ==> <QuerySet [{'design_id':1, 'n_uses': 2]>
		)
			# Create a list that formats design_usage to include Design instances (instead of design_ids)
		cleaned_design_usage = [
			{
				# Use design_id to retrieve Design instance
				'design':Design.objects.get(pk=item['design_id']),
				# Keep the n_uses 
				'n_uses':item['n_uses']
			} 
			for item in design_usage 
		] # ==> [{'design': <Design: Abstract>, 'n_uses': 2},{...}]
		context['design_usage'] = cleaned_design_usage
		usage_by_day = (
			Usage.objects
			.exclude(card__owner=None)
			.values(unique_day=TruncDay('date_used'))
			.annotate(n_taps=Count('unique_day'))
			.order_by('-unique_day')
		)
		context['usage_by_day'] = usage_by_day
		print('Stats.get_context_data() => ', context)
		return context
	


def config_plotly(request):
	plotly_graphs = []
	
	# Define querysets here
	daily_usage_qs = (
		Usage.objects
		.exclude(card__owner=None)
		.values(x=TruncDay('date_used'))
		.annotate(y=Count('x'))
		.order_by('-y')
	)
	
	user_taps_qs = (
		Usage.objects
		.exclude(card__owner=None)
		.values('card__owner_id')
		.annotate(y=Count('card__owner_id'))
		.order_by('-y')[0:3]
	)
	
	# Clean querysets here
	cleaned_user_taps = [
		{
			# Use card__owner_id to retrieve Owner instance 
			'user': Owner.objects.get(pk=item['card__owner_id']).__str__(),
			# Keep n_card_taps
			'n_card_taps': item['y']
		} 
		for item in user_taps_qs
	]
	daily_usage_graph = __extract_graph_data(daily_usage_qs, type="line", target_elem="__plot_daily_usage")
	user_taps_graph = __extract_graph_data(cleaned_user_taps, type="bar", target_elem="__plot_user_taps")
	
	# Register graphs to plotly graphs list
	plotly_graphs.append(daily_usage_graph)
	plotly_graphs.append(user_taps_graph)
	
	return JsonResponse(plotly_graphs, safe=False)

# Loop through given list/queryset  and extract graph object
def __extract_graph_data(queryset, target_elem="", type='scatter'):
	graph_data = {
		'target_elem' : target_elem,
		'traces' : [
			{
				'x' : [],
				'y' : [],
				'type' : type,
			}
		],
	}

	# Some querysets may come with dictionaries w/ more than 2 keys
	for coordinate in queryset:
		print(f"coordinate: {coordinate}\n queryset: {queryset}")
		if len(coordinate.keys()) == 2:
			x_series_key = list(coordinate.keys())[0]
			y_series_key = list(coordinate.keys())[1]
			graph_data['traces'][0]['x'].append(coordinate[x_series_key])
			graph_data['traces'][0]['y'].append(coordinate[y_series_key])
	print('__extract_graph_data:', graph_data)
	return graph_data 

### IP9: APIs + JSON Endpoints + Server-Side Charts

def daily_usage(request):
	"""
	GET /api/daily_usage
	Return unique days and number of card taps for bar graph
	""" 
	# Create a queryset
	daily_usage_qs = (
		Usage
		.objects
		.exclude(card__owner=None)
		.values(unique_day=TruncDay('date_used')) # unique days
		.annotate(n_card_taps=Count('card'))
		.order_by('-unique_day')
	)
	# Let's break the queryset into two lists (denotes the x, and y series)
	unique_days = [ day['unique_day'].strftime("%Y-%m-%d") for day in daily_usage_qs ]
	n_card_taps = [ day['n_card_taps'] for day in daily_usage_qs ]
	# And return as JSON
	return JsonResponse({"labels": unique_days, "values": n_card_taps}, safe=True)


def daily_usage_png(request):
	"""
	Creates a bar graph png using matplotlib and the json data from my daily_usage fbv

	"""
	# Build the absolute uri that I'll pull the json from
	api_uri = request.build_absolute_uri(reverse("api_daily_usage_view"))
	# print(api_uri) ==> http://localhost:8000/api/daily_usage/bar_graph.png
	# Let's grab the json data from that uri
	with urllib.request.urlopen(api_uri) as api_json_response:
		pyth_dict = json.load(api_json_response) # Parse string to python dict

	x_series = pyth_dict['labels']
	y_series = pyth_dict['values']

	# And start plotting
	x = range(len(x_series))
	fig, ax = plt.subplots(figsize=(6.5, 3.2), dpi=150)
	ax.bar(x_series, y_series, color="#13294B")
	ax.set_title("Taps per day")
	ax.set_ylabel("# Taps")
	ax.set_xticklabels(x_series, rotation=45, ha="right")
	fig.tight_layout()

	buf = BytesIO()
	fig.savefig(buf, format="png")
	plt.close(fig)
	buf.seek(0)
	return HttpResponse(buf.getvalue(), content_type="image/png")

        
        
