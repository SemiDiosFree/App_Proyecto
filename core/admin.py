from django.contrib import admin
from .models import HomeView

# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('title',)

    class Media:
        css = {
            'all': ('core/css/custom_ckeditor.css',)
        }
admin.site.register(HomeView, HomeAdmin)