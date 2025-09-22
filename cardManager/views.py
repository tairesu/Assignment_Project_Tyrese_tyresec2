from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.template import loader
import stripe
from django.views.decorators.csrf import csrf_exempt
from cardManager.models import (
	Card,
	Profile
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
		base_url = 'http://localhost:8000'
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
	print("Stripe post checkout success")
	print("stripe session_id", request.GET['session_id'])
	return render(request, 'cardManager/success.html')

def cancelled(request):
	return render(request, 'cardManager/cancelled.html')
