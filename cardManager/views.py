from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from cardManager.models import (
	Card,
)
# Create your views here.
def card_detail(request,card_token):
	print('card_detail request: ', request)
	card = Card.objects.filter(token=card_token)[0]
	show_profile = card.show_profile
	is_owned = not (card.user == None)
	is_redirecting = not (card.reroute_url == None)
	context = {"card":card}

	if is_owned and not show_profile:
		context["decision"] = f"Redirecting to {card.reroute_url}"

	elif is_owned and show_profile: 
		context["decision"] = f"Redirecting to {card.user}'s Profile"

	elif not is_owned:
		context["decision"] = f"Redirecting to {card_token}/activate"
	else:
		context["decision"] = f"Card token not found"

	template = loader.get_template("cardManager/base.html")
	output = template.render(context, request)
	return HttpResponse(output)