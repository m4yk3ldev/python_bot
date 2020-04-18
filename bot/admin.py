from django.contrib import admin

# Register your models here.

from .models import Profile
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name', 'username')
    form = ProfileForm
