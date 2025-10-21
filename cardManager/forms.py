from django import forms
from cardManager.models import Card


class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		exclude = ['token','owner','design']

