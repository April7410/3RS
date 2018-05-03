from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
	search_fields = [ 'email' ]
	form = UserAdminChangeForm # edit view
	add_form = UserAdminCreationForm # create view

	# The fields to be used in displaying the User model.
	# These override the definitions on the base UserAdmin
	# that reference specific fields on auth.User.
	list_display = ('email', 'name', 'student', 'staff', 'admin')
	list_filter = ('admin', 'staff', 'student')
	fieldsets = (
		("Account Info", {'fields': ( 'email', 'password', )}),
		('Personal Info', {'fields': ( 'name', )}),
		('Permissions', {'fields': ( 'student', 'staff', 'admin',)}),
	)
	# add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	# overrides get_fieldsets to use this attribute when creating a user.
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password1', 'password2', 'name', )}
		),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


# Register your models here.
admin.site.register(User, UserAdmin)