from django.contrib import admin
from .models import (
	Profile,
	Card,
	Design,
	Usage,
 	Request
)


admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Design)
admin.site.register(Usage)
admin.site.register(Request)

