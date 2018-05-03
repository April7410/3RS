from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
	def create_user(self, email, name, password=None, is_student=False, is_staff=False,
					is_admin=False, phone_number=None, fax_number=None):
		if not email:
			raise ValueError("Users must have an email")
		if not name:
			raise ValueError("Users must have a name")
		if not password:
			raise ValueError("Users must have a password")
		
		user = self.model(
			email = self.normalize_email(email),
			name = name,
		)
		user.set_password(password) # How to set/change change password
		user.student = is_student
		user.staff = is_staff
		user.admin = is_admin
		user.save(using=self._db)
		return user

	def create_student_user(self, email, name, password):
		user = self.create_user(
			email,
			name,
			password,
			phone_number,
			fax_number,
			is_student=True,
		)
		return user
	
	def create_staff_user(self, email, name, password):
		user = self.create_user(
			email,
			name,
			password,
			phone_number,
			fax_number,
			is_staff=True
		)
		return user
	
	def create_superuser(self, email, name, password):
		user = self.create_user(
			email,
			name,
			password,
			phone_number,
			fax_number,
			is_staff=True,
			is_admin=True,
		)
		return user


class User(AbstractBaseUser):
	email		= models.EmailField(unique=True, max_length=255, blank=False, null=True)
	name		= models.CharField(max_length=255, blank=False, null=True)
	student		= models.BooleanField(default=False)
	staff		= models.BooleanField(default=False)
	admin		= models.BooleanField(default=False)
	phone_number = models.IntegerField(blank=True, null=True)
	fax_number	= models.IntegerField(blank=True, null=True)
	timestamp	= models.DateTimeField(auto_now_add=True)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = [ 'name', ]
	
	objects = UserManager()
	
	def __str__(self):
		return self.name + " (" + self.email + ")"
	
	def get_full_name(self):
		return self.name
	
	def has_perm(self, perm, obj=None):
		return True
	
	def has_module_perms(self, app_label):
		return True

	@property
	def is_student(self):
		return self.student
	
	@property
	def is_staff(self):
		return self.staff
	
	@property
	def is_admin(self):
		return self.admin

