import stripe
from datetime import datetime
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, views as auth_views
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.views.generic.base import ContextMixin, View
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from cardManager.forms import (
	UserForm,
	CardForm,
	ProfileForm
)
from cardManager.models import (
	Card,
	Profile,
	User
)


# Handles redirects for a scanned card matching card_token 
def card_detail(request,card_token):
	card = Card.objects.get(token=card_token)
	is_owned = not (card.user == None)
	is_redirecting = not (card.reroute_url == "")
	if is_owned and not card.show_profile and is_redirecting:
		return redirect(card.reroute_url)
	elif is_owned and card.show_profile: 
		return redirect('profile_view', profile_slug=card.user.profile.profile_slug)
	elif not is_owned:
		return redirect('card_activate_view', card_token=card_token)	
	elif is_owned and not is_redirecting:
		return redirect('card_update_view',pk=card.pk)
	else:
		return render(request, 'cardManager/invalid_token.html')

 
# Render profile template using the slugs instead of pk
class ProfileDetail(DetailView):
	model = Profile
	template_name = 'cardManager/profile.html'
	slug_field = 'profile_slug'
	slug_url_kwarg = 'profile_slug'

class ProfileUpdate(LoginRequiredMixin, UpdateView):
	model = Profile
	form_class = ProfileForm
	template_name = 'cardManager/profile_update.html'
	
	def get_success_url(self):
		# Grab the profile_slug from this obj
		profile_slug = self.object.profile_slug
		# Send slug over to profile detail view
		return reverse_lazy('profile_view', kwargs={'profile_slug': profile_slug })

class ProfileCreate(LoginRequiredMixin, CreateView):
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
		profile.user = self.request.user
		profile.save()
		return super().form_valid(form)


# Renders card activate template with card
def card_activate(request, card_token):
	card = Card.objects.filter(token=card_token)[0]
	is_activated = not (card.user == None)
	if is_activated:
		#Redirect to card view url
		return redirect('card_view', card_token=card_token)
	context = {
		'card': card,
	}
	# Save card_token and id into a request session 
	request.session['activating_card_token'] = card_token
	request.session['activating_card_id'] = card.card_id
	request.session.save()
	return render(request, 'cardManager/activate.html', context)


# Class view for editing Cards
class CardUpdate(LoginRequiredMixin, UpdateView):
	model = Card
	form_class = CardForm
	success_url = reverse_lazy('dashboard_view')
	template_name = "cardManager/card_update.html"


# Renders dashboard template with user cards
class UserDashboard(LoginRequiredMixin, ContextMixin, View):
	template_name = 'cardManager/dashboard.html'

	def get(self, request, **kwargs):
		context = self.get_context_data(**kwargs)
		return render(request, self.template_name, context)

	# I need to alter the context that goes to the dashboard template
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user_id = self.request.user.pk
		user_cards = Card.objects.filter(user_id=user_id)
		context['user_cards'] = user_cards
		return context


# Renders post stripe success template 
def success(request):
	return render(request, 'cardManager/success.html')


# Renders cancalled payment template
def cancelled(request):
	return render(request, 'cardManager/cancelled.html')


# View that gets publishable key for stripe
@csrf_exempt
def stripe_config(request):
	if request.method == 'GET':
		stripe_config = {
			'publishable_key' : settings.STRIPE_PUBLISHABLE_KEY
		}
		return JsonResponse(stripe_config, safe=False)
			

# Create a new Checkout session ID
@csrf_exempt
def create_checkout_session(request):
	if request.method == 'GET':
		base_url = 'http://localhost:8000'
		stripe.api_key = settings.STRIPE_SECRET_KEY
		try:
			checkout_session = stripe.checkout.Session.create(
				success_url=base_url + '/card/' + str(request.session['activating_card_id']) + '/update/?session_id={CHECKOUT_SESSION_ID}',
				cancel_url=base_url + '/cancelled/',
				mode='payment',
				customer_email=request.user.email,
				metadata={
					'card_id':request.session['activating_card_id'],
					'card_token':request.session['activating_card_token'],
					'user_id':request.user.id
				},
				line_items=[{
                        'quantity': 1,
                        'price': 'price_1PUzvPAAVj3eEQONrfXv9xPy' 
                    }]
			)
			#checkout_session id is needed for stripe to generate a checkout session 
			return JsonResponse({'sessionId': checkout_session['id']})
		except Exception as e:
			print('create_checkout_session error:', e)
			return JsonResponse({'error': str(e)})


# Handles payment confirmation 
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
    	#Grab user_id and card_id from Stripes Metadata
    	session = event['data']['object']
    	card_id = session['metadata'].get('card_id')
    	user_id = session['metadata'].get('user_id')
    	# Retrieve the matching User and Card
    	user = User.objects.get(id=user_id)
    	card = Card.objects.get(card_id=card_id)
    	# Save the user attribute of the matching Card model
    	card.user = user
    	card.save()

    return HttpResponse(status=200)


# Class view for new user registration form
class UserRegistration(CreateView):
	form_class = UserForm
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


class LoginView(auth_views.LoginView):
	template_name = 'cardManager/login.html'
	success_url = reverse_lazy('dashboard_view')

	def get_success_url(self):
		return self.request.GET.get('next') or self.success_url
	#Grab the next url parameter as context
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['nextUrlParam'] = self.request.GET.get('next') or None
		print("Context Data from LoginView:", context)
		return context


