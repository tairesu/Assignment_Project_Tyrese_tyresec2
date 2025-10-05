from django.contrib import admin
from .models import (
	Profile,
	Card,
	Owner,
	Design
)


admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Owner)
admin.site.register(Design)

