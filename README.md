# NOTE
1. created_by is nullable in current Sport model. This is only for development convenience. In production, it must be non-nullable

# BUGS



# Places to include emails
1. When a slot is updated, notify everyone who booked that slot

2. Successfully booked a slot

3. Booking cancelled by an admin 

# TODO
1. Change sidebar
2. Limit choices of facilities to selected sport in CreateNewSlotForm
3. decide duration: FloatField ok or not since timeStart - timeEnd should match duration in CreateNewSlotForm
4. Add a note explaining reason for cancellation in email when staff cancels a booking

# MODELS

TBD


# CODE SNIPPETS

1. Custom User Model in Django - https://testdriven.io/blog/django-custom-user-model/#admin



_users/admin.py_   

```
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
```

