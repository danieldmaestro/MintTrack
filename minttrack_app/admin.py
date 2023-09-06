from django.contrib import admin

from .models import Item, Category, Transaction, Budget, Goal, GoalTransaction

# Register your models here.

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

