import stripe
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth import login, views as auth_views
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, ListView
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from cardManager.forms import (
	UserForm,
	CardForm
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


# Renders Profile template w/ matching Profile data
def profile_detail(request, profile_slug):
	profile = Profile.objects.filter(profile_slug=profile_slug)[0]
	context = {"profile":profile}
	return render(request, "cardManager/profile.html", context)


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
	template = loader.get_template("cardManager/activate.html")
	output = template.render(context, request)
	return HttpResponse(output)


# Renders dashboard template with context cards
def dashboard(request):
	cards = Card.objects.filter(user=request.user)
	context = {
		'cards': [card for card in cards]
	}
	return render(request, 'cardManager/dashboard.html', context)


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
	model = User
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


# Class view for editing Cards
class CardUpdate(UpdateView):
	model = Card
	form_class = CardForm
	success_url = reverse_lazy('dashboard_view')
	template_name = "cardManager/card_update.html"


class LoginView(auth_views.LoginView):
	template_name = 'cardManager/login.html'