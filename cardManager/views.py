from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from cardManager.models import (
	Card,
)
# Create your views here.
def card_detail(request,card_token):
	print('card_detail request: ', request)
	cards = Card.objects.filter(token=card_token)
	context = {"cards":cards}
	template = loader.get_template("cardManager/base.html")
	output = template.render(context, request)
	return HttpResponse(output)