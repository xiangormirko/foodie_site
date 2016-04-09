from django.contrib import admin

# Register your models here.

from .models import List, Restaurant, Cuisine, Chat
from .models import UserProfile

class RestInline(admin.StackedInline):
    model = Restaurant

class ListAdmin(admin.ModelAdmin):
    inlines = [RestInline,]


admin.site.register(List, ListAdmin)
admin.site.register(Restaurant)
admin.site.register(UserProfile)
admin.site.register(Cuisine)
admin.site.register(Chat)