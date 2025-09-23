from django.contrib.auth.models import User
from django import forms
from .models import (
	Card
)

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password']


class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		fields = ['reroute_url','show_profile','alias']