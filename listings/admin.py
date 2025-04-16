from django.contrib import admin
from .models import Listing
from .models import Profile
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Listing)
admin.site.register(Profile)

class ProfileInline(admin.StackedInline):
	model = Profile
	fk_name = 'user'

class UserAdmin(admin.ModelAdmin):
	model = User
	field = ['username', 'first_name', 'last_name', 'email']
	inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)