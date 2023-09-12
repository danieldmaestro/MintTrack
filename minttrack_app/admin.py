from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import Item, Category, Transaction, Budget, Goal, GoalTransaction, User

# Register your models here.

class UserAdmin(BaseUserAdmin):

    ordering = ('email',)  # Set the ordering field to 'email'
    list_display = ('email', 'is_staff', 'first_name', 'last_name', 'is_active')  # Add 'role', 'is_staff', and 'is_active' to the list_display field
    list_filter = ('is_staff', 'is_superuser',)  # Add 'role' to the list_filter field
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
        ("Dates", {"fields": ("last_login",)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',),
        }),
    )


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    
    
class GoalTransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'goal']
    


admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(Goal)
admin.site.register(GoalTransaction, GoalTransactionAdmin)
admin.site.register(User, UserAdmin)


