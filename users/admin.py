from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('id', 'username', 'email', 'is_active', 'is_verify_email')
    list_filter = ('is_verify_email', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)
    readonly_fields = ('last_login', 'date_joined', 'id')
    fieldsets = (
        ('Personal Info', {
            'fields': ('id', 'username', 'email', 'first_name', 'last_name', 'is_verify_email')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active'),
        }),
        ('Change Password', {
            'fields': ('password',),
            'classes': ('collapse',),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )



admin.site.register(User, CustomUserAdmin)

