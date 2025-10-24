from django import forms
from cardManager.models import (
	Card,
	Profile
)
from django.core.exceptions import ValidationError


class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		exclude = ['token','owner','design']

	def clean(self):
		data = super().clean()
		is_reroute_set = not (data['reroute_url'] == "")
		is_profile_set = data['show_profile']
		if is_profile_set and is_reroute_set:
			self.add_error("reroute_url","Reroute URL not needed if profile is set")
		elif not is_profile_set and not is_reroute_set:
			self.add_error("reroute_url","Reroute URL needed")

		return data

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'

