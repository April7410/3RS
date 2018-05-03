from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField


class LoginForm(forms.Form):
	email		= forms.EmailField(label='Email')
	password	= forms.CharField(label='Password', widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
	password1	= forms.CharField(label='Confirm Password',
								  widget=forms.PasswordInput(attrs = {'placeholder': 'Enter password here...'}))
	password2	= forms.CharField(label='Confirm Password',
								  widget=forms.PasswordInput(attrs = {'placeholder': 'Enter password here...'}))
	
	class Meta:
		model = User
		fields = ( 'email',
				  'name',
				  'password1',
				  'password2',
				  'phone_number',
				  'fax_number',
		)

	def save(self, commit=True):
		# Create the model, but don't save the data because it has to be edited
		user = super(RegisterationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.password = set_password(self.cleaned_data["password1"])
		user.name = self.cleaned_data['name']
		
		if commit:
			user.save()
		return user
	
	def clean_password(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and passowrd2 and password1 != password2:
			raise forms.ValidationError("Passwords do not match")
		return password


class UserAdminCreationForm(forms.ModelForm):
	"""A form for creating new users. Includes all the required
	fields, plus a repeated password."""
	password1	= forms.CharField(label='Password', widget=forms.PasswordInput)
	password2	= forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = ( 'email', 'name', 'student', 'staff', 'admin', )

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		# Save the provided password in hashed format
		user = super(UserAdminCreationForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class UserAdminChangeForm(forms.ModelForm):
	"""A form for updating users. Includes all the fields on
	the user, but replaces the password field with admin's
	password hash display field."""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ( 'email', 'password', 'name', 'student', 'staff', 'admin' )

	def clean_password(self):
		# Regardless of what the user provides, return the initial value.
		# This is done here, rather than on the field, because the
		# field does not have access to the initial value
		return self.initial["password"]