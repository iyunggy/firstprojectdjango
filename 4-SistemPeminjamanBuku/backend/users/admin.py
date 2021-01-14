from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from import_export.admin import ImportExportModelAdmin

class CustomUserAdmin(BaseUserAdmin, ImportExportModelAdmin):
    fieldsets = (
        (None, {'fields': ('created_on','email', 'password','fullname','phone', 'status','tanggal_lahir',)}),
        ('Permissions', {'fields': ('is_staff','is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':('created_on','email','fullname', 'phone','status','tanggal_lahir','password1', 'password2',)
        }),
    )
    list_display = ('created_on','email', 'fullname','status',  )

    list_filter = ('email', 'status',)
    search_fields = ('email','fullname', 'status',  )
    ordering = ('created_on','status', 'email',)
    
admin.site.register(CustomUser, CustomUserAdmin)
