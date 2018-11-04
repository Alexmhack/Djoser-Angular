from django.db import models
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

def clean_email(value):
	user = User.objects.filter(email=value)
	if user.exists():
		raise ValidationError('A user with that email address already exists.')

	return value


class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		"""
		Create and save a user with the given username, email, and password.
		"""
		if not username:
			raise ValueError('The given username must be set')
		email = self.normalize_email(email)
		username = self.model.normalize_username(username)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staffuser(self, username, email, password):
		"""
		Creates and saves a staff user with the given email and password.
		"""
		user = self.create_user(
			username=self.normalize_email(username),
			email=self.normalize_email(email),
			password=password,
		)
		user.staff = True
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser):
	username_validator = UnicodeUsernameValidator()

	username = models.CharField(
		_('username'),
		max_length=150,
		unique=True,
		help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
		validators=[username_validator],
		error_messages={
			'unique': _("A user with that username already exists."),
		},
	)

	email = models.EmailField(
		_('email address'),
		unique=True,
		max_length=255,
		error_messages={
			'unique': _("A user with that email address already exists."),
		},
	)
	is_staff = models.BooleanField(
		_('staff status'),
		default=False,
		help_text=_('Designates whether the user can log into this admin site.'),
	)
	is_active = models.BooleanField(
		_('active'),
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		),
	)
	is_superuser = models.BooleanField(
		_('superuser status'),
		default=False,
		help_text=_(
			'Designates that this user has all permissions without '
			'explicitly assigning them.'
		),
	)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def clean(self):
		super().clean()
		self.email = self.__class__.objects.normalize_email(self.email)

	def get_full_name(self):
		"""
		Return the first_name plus the last_name, with a space in between.
		"""
		return str(self.email)

	def get_short_name(self):
		"""Return the short name for the user."""
		return self.username

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""Send an email to this user."""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True
