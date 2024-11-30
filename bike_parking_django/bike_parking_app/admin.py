from django.contrib import admin
from .models import CustomUser,BikeRackData,Achievements,Badge,NewMarker,DeleteMarker
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(CustomUser)
# @admin.register(CustomUser)
# class CustomAdminUser(UserAdmin):
#         add_form = CustomUserCreationForm
#         form = CustomUserChangeForm
        
#         model = CustomUser

admin.site.register(BikeRackData)
admin.site.register(Achievements)
admin.site.register(Badge)
admin.site.register(NewMarker)
admin.site.register(DeleteMarker)

