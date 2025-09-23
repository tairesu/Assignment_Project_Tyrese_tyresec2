import stripe
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.generic import CreateView
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from cardManager.forms import (
	UserForm
)
from cardManager.models import (
	Card,
	Profile,
	User
)
# Create your views here.
def card_detail(request,card_token):
	print('card_detail request: ', request)
	card = Card.objects.filter(token=card_token)[0]
	is_owned = not (card.user == None)
	is_redirecting = not (card.reroute_url == None)
	context = {"card":card}

	if is_owned and not card.show_profile:
		return redirect(card.reroute_url)

	elif is_owned and card.show_profile: 
		user_profile = card.user.profile
		user_profile_slug = user_profile.profile_slug
		return redirect('profile_view', profile_slug=user_profile_slug)

	elif not is_owned:
		return redirect('card_activate_view', card_token=card_token)
		

	template = loader.get_template("cardManager/base.html")
	output = template.render(context, request)
	return HttpResponse(output)

def profile_detail(request, profile_slug):
	profile = Profile.objects.filter(profile_slug=profile_slug)[0]
	context = {"profile":profile}
	return render(request, "cardManager/profile.html", context)

def card_activate(request, card_token):
	card = Card.objects.filter(token=card_token)[0]
	is_activated = not (card.user == None)
	if is_activated:
		#Go to card view url
		return redirect('card_view', card_token=card_token)
	context = {
		'card': card,
	}
	request.session['activating_card_token'] = card_token
	template = loader.get_template("cardManager/activate.html")
	output = template.render(context, request)
	return HttpResponse(output)

	
#View that gets publishable key from stripe
@csrf_exempt
def stripe_config(request):
	if request.method == 'GET':
		stripe_config = {
			'publishable_key' : settings.STRIPE_PUBLISHABLE_KEY
		}
		return JsonResponse(stripe_config, safe=False)
			

@csrf_exempt
#Create a new Checkout session ID
def create_checkout_session(request):
	if request.method == 'GET':
		base_url = 'http://127.0.0.1:8000'
		stripe.api_key = settings.STRIPE_SECRET_KEY
		try:
			checkout_session = stripe.checkout.Session.create(
				success_url=base_url + '/success?session_id={CHECKOUT_SESSION_ID}',
				cancel_url=base_url + '/cancelled/',
				mode='payment',
				line_items=[{
                        'quantity': 1,
                        'price': 'price_1PUzvPAAVj3eEQONrfXv9xPy' 
                    }]
			)
			#checkout_session id is needed for stripe to redirect to stripe checkout 
			return JsonResponse({'sessionId': checkout_session['id']})
		except Exception as e:
			return JsonResponse({'error': str(e)})

def success(request):
	return render(request, 'cardManager/success.html')

def cancelled(request):
	return render(request, 'cardManager/cancelled.html')

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
    print("stripe_webhook:",event['type'])
    print("activating card_token:",request.session['activating_card_token'])
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)


class UserRegistration(CreateView):
	model = User
	form_class = UserForm
	template_name = "cardManager/register.html"
	success_url = "dashboard/"

	def get_success_url(self):
		#Route to dashboard if next parameter is not defined
		return self.request.GET.get('next') or self.success_url

	def form_valid(self, form):
		user = form.save(commit=False)
		user.save();
		#Log the user in 
		login(self.request, user)

		return super().form_valid(form)



