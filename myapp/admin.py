from django.contrib import admin

# Register your models here.

from .models import Information


class InformationAdmin(admin.ModelAdmin):
    list_display = ('company','phone','web','mail')
    search_fields = ('company','phone','web','mail')
    
admin.site.register(Information, InformationAdmin)
    