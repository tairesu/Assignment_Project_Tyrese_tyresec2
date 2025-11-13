from django import forms
from cardManager.models import (
	Card,
	Profile,
 	Request
)
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CardForm(forms.ModelForm):
	class Meta:
		model = Card
		exclude = ['token','owner','design']

	def clean(self, **kwargs):
		data = super().clean(**kwargs)
		is_reroute_set = self.fields['reroute_url'].clean(self.data['reroute_url'])
		is_profile_set = data['show_profile']
		if is_profile_set and is_reroute_set:
			self.add_error("reroute_url","Reroute URL not needed if profile is set.")
		elif not is_profile_set and not is_reroute_set:
			self.add_error("reroute_url","Reroute URL needed.")

		return data


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
  

class RequestForm(forms.ModelForm):
	class Meta:
		model = Request
		fields = ['preset_design','custom_design', 'custom_design_rear', 'card_qty']

# =====================================================================================================
# A11 
# =====================================================================================================

class OwnerSignUpForm(UserCreationForm):
	"""
	Form for django User auth table
	"""
	email = forms.EmailField(required=True, help_text="We'll use this email to contact you")

	class Meta:
		model = User
		fields = ['first_name','last_name','username','email','password1','password2']