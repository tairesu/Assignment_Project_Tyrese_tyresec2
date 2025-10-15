from django import forms
from cardManager.models import Card

class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		fields = ['alias','show_profile','reroute_url']