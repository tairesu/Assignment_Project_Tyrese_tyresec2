from django.contrib import admin
from .models import (
	Profile,
	Card,
	Owner
)


admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Owner)

