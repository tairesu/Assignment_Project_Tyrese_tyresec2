import stripe
from datetime import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, views as auth_views
from django.http import HttpResponse
from django.http.response import JsonResponse
# from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, ListView, DetailView, RedirectView
from django.views.generic.base import ContextMixin, View
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from cardManager.forms import (
	OwnerForm,
	CardForm,
	ProfileForm
)
from cardManager.models import (
	Card,
	Profile,
	Owner,
	Usage
)

def __add_to_usage(request, card):
	print('\ninit\'d __add_to_usage')
	new_use = Usage(card=card)
	new_use.save()

# Handles redirects for a scanned card matching card_token 
def card_detail(request,card_token):
	card = get_object_or_404(Card, token=card_token)
	__add_to_usage(request, card)
	is_owned = not (card.owner == None)
	is_redirecting = not (card.reroute_url == "")

	if is_owned and not card.show_profile and is_redirecting:
		return redirect(card.reroute_url)
	elif is_owned and card.show_profile:
		return redirect('profile_view', profile_slug=card.owner.profile.profile_slug)
	elif is_owned and not is_redirecting:
		return redirect('card_update_view',pk=card.pk)
	elif not is_owned:
		return redirect('card_activate_view', card_token=card_token)	


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
	
	def get_success_url(self):
		# Grab the profile_slug from this obj
		profile_slug = self.object.profile_slug
		# Send slug over to profile detail view
		return reverse_lazy('profile_view', kwargs={'profile_slug': profile_slug })

class ProfileCreate(CreateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'cardManager/profile_create.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		timenow = datetime.now().strftime("%H:%M:%S")
		print(f'\n[{ timenow }] [ProfileCreate] context: ', context, '\n')

	def get_success_url(self):
		# Grab the profile_slug from this obj
		profile_slug = self.object.profile_slug
		# Send slug over to profile detail view
		return reverse_lazy('profile_view', kwargs={'profile_slug': profile_slug })

	def form_valid(self,form):
		profile = form.save(commit=False)
		profile.owner = self.request.owner
		profile.save()
		return super().form_valid(form)


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


# Class view for editing Cards
class CardUpdate(UpdateView):
	model = Card
	form_class = CardForm
	success_url = reverse_lazy('dashboard_view')
	template_name = "cardManager/card_update.html"


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



# Class view for new user registration form
class UserRegistration(CreateView):
	form_class = OwnerForm
	template_name = "cardManager/register.html"
	success_url = reverse_lazy('dashboard_view')

	#Changes default success_url
	def get_success_url(self):
		#Route to dashboard if next parameter is not defined
		return self.request.GET.get('next') or self.success_url

	# Login the user in when form is valid
	def form_valid(self, form):
		user = form.save(commit=False)
		user.save();
		#Log the user in 
		login(self.request, user)
		return super().form_valid(form)

	# Forwards next URL paremeter
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['nextUrlParam'] = self.request.GET.get('next') or None
		return context
