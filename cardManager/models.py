from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User


class Profile(models.Model):
	profile_id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', blank=True)
	name = models.CharField(max_length=60)
	bio = models.TextField(blank=True)
	profile_slug = models.CharField(max_length=25)
	cell = models.CharField(max_length=12, blank=True)
	linked_in = models.URLField(max_length=200, blank=True)
	snapchat = models.CharField(max_length=50, blank=True)
	profile_photo = models.ImageField(upload_to='userPhotos/profile/', blank=True)
	banner_photo = models.ImageField(upload_to='userPhotos/banners/', blank=True)
	instagram = models.CharField(max_length=50, blank=True)
	whatsapp = models.CharField(max_length=12, blank=True)
	date_created = models.DateTimeField(default=timezone.now, editable=False)

	class Meta:
		constraints = [
			UniqueConstraint(fields=['profile_slug'], name='unique_profile_slug')
		]

	def __str__(self):
		return f"{self.profile_slug}"

	def get_update_url(self):
		return reverse('profile_update_view', kwargs={'pk': self.pk})


class Card(models.Model):
	card_id = models.AutoField(primary_key=True)
	token = models.CharField(max_length=7)
	user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cards',null=True, blank=True)
	alias = models.CharField(max_length=60, blank=True)
	show_profile = models.BooleanField(default=False)
	front_design = models.ImageField(upload_to='cardDesigns/', blank=True)
	rear_design = models.ImageField(upload_to='cardDesigns/', blank=True)
	reroute_url = models.URLField(max_length=200, blank=True)

	class Meta:
		constraints = [
			UniqueConstraint(fields=['token'], name='unique_card_token')
		]

	def __str__(self):
		return f"Card {self.token}" if self.user else f"[Unclaimed] Card {self.token}"

	def get_update_url(self):
		return reverse('card_update_view', kwargs={'pk': self.pk})