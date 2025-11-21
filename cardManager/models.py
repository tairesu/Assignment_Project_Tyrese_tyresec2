from cardManager.utils import gen_card_token as gen_token
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.contrib.auth.models import User


class Owner(models.Model):
	owner_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100, blank=False)
	last_name = models.CharField(max_length=100, blank=False) 
	email = models.EmailField(max_length=200, blank=False, unique=True)
	pword = models.CharField(max_length=128, blank=False)
	date_created = models.DateTimeField(default=timezone.now, editable=False)
	last_login = models.DateTimeField(default=timezone.now, editable=False )

	def __str__(self):
		return f'{self.first_name} {self.last_name}'


class Profile(models.Model):
	profile_id = models.AutoField(primary_key=True)
	owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
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

	def get_absolute_url(self):
		return reverse('profile_view', kwargs={'profile_slug': self.profile_slug})
	
	def get_update_url(self):
		return reverse('profile_update_view', kwargs={'profile_slug': self.profile_slug})


class Design(models.Model):
	design_id = models.AutoField(primary_key=True)
	name = models.CharField(blank=False, null=False, max_length=50)
	front_design = models.ImageField(upload_to='cardDesigns/', blank=True)

	def __str__(self):
		return self.name


class Card(models.Model):
	card_id = models.AutoField(primary_key=True)
	token = models.CharField(max_length=7, default=gen_token, blank=False,null=False, unique=True)
	owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cards',null=True, blank=True, default=1)
	alias = models.CharField(max_length=60, blank=True)
	show_profile = models.BooleanField(default=False)
	reroute_url = models.URLField(max_length=200, blank=True)
	design = models.ForeignKey(Design, on_delete=models.PROTECT, related_name='cards', null=False, blank=False)

	class Meta:
		constraints = [
			UniqueConstraint(fields=['owner','alias'], name='unique_card_alias')
		]

	def __str__(self):
		return f"Card {self.token}" if self.owner else f"[Unclaimed] Card {self.token}"

	def get_absolute_url(self):
		return reverse('card_view', kwargs={'card_token': self.token})

	def get_update_url(self):
		return reverse('card_update_view', kwargs={'card_token': self.token})


class Usage(models.Model):
	card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='usage' )
	date_used = models.DateTimeField(default=timezone.now, editable=False)

	def __str__(self):
		return f'{self.date_used} {self.card}'

# A9 
class Request(models.Model):
    status_choices = [
        ('pending','Pending'),
        ('printed','Printed'),
        ('Adhered','Adhered'),
        ('complete','Complete'),
    ]
    request_id = models.AutoField(primary_key=True)
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    preset_design = models.ForeignKey(Design, related_name="requests", on_delete=models.PROTECT,null=True, blank=True)
    custom_design = models.ImageField(upload_to='userPhotos/customDesigns/', blank=True)
    custom_design_rear = models.ImageField(upload_to='userPhotos/customDesigns/', blank=True)
    owner = models.ForeignKey(Owner, related_name="requests", on_delete=models.PROTECT, blank=False)
    card_qty = models.IntegerField(default=1)
    status = models.CharField(choices=status_choices, default='Pending', max_length=10)
    
    
    def __str__(self):
        return f"{self.owner} requested {self.card_qty} card(s)" 
    
    def get_absolute_url(self):
        return reverse("order_detail_view", kwargs={"pk": self.pk})
	