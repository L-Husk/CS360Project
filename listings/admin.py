from django.contrib import admin
from .models import Listing, Profile, Pending
from django.contrib.auth.models import User
# Register your models here.

admin.site.register(Listing)
admin.site.register(Profile)
admin.site.register(Pending)

class ProfileInline(admin.StackedInline):
	model = Profile
	fk_name = 'user'

class UserAdmin(admin.ModelAdmin):
	model = User
	field = ['username', 'first_name', 'last_name', 'email']
	inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)