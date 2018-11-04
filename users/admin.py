from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .forms import UserAdminCreationForm, UserAdminChangeForm, RegisterForm
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(_('Personal info'), {'fields': ('email',)}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password'),
		}),
	)
	form = UserAdminChangeForm
	add_form = UserAdminCreationForm
	list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
	list_filter = ('is_staff', 'is_superuser', 'is_active')
	search_fields = ('username', 'email')
	ordering = ('username',)
	filter_horizontal = ()
