from django import forms
from .models import (
	Card,
	Profile,
	Owner
)

class OwnerForm(forms.ModelForm):
	class Meta:
		model = Owner
		fields = ['first_name','last_name','email','pword']


class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		fields = ['reroute_url','show_profile','alias']

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ['user','date_created']