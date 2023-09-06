import locale

from django.db.models import Sum

from rest_framework import serializers

from .models import Item, Category, Transaction, Budget, Goal

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['name', 'category']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name', ]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['item', 'amount', 'date', 'category_name', 'item_name', 'time']

    def get_category_name(self, obj):
        return obj.item.category.name

    def get_item_name(self, obj):
        return obj.item.name
    
    def get_time(self, obj) -> str:
        date = obj.time
        formatted_time = date.strftime('%I:%M %p')
        return formatted_time
    
    def get_date(self, obj) -> str:
        date = obj.date
        formatted_date = date.strftime('%d/%m/%Y')
        return formatted_date


class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    saved = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = ['name', 'target_amount', 'target_savings', 'saved', 'progress', 'target_date']

    def get_progress(self, obj):
        return f"{obj.progress()}%"
    
    def get_saved(self, obj):
        return locale.format_string("%d", obj.saved(), grouping=True)
    

class ItemBudgetSerializer(serializers.ModelSerializer):
    spent = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Budget
        fields = ['item', 'amount', 'month', 'spent', ]

    def get_spent(self, obj):
        spent_amount = Transaction.objects.filter(date__months=obj.month, item=obj.item).aggregate(total_amount=Sum('amount'))
        return spent_amount['total_amount']
    
    def get_category_name(self, obj):
        return obj.item.category.name

    def get_item_name(self, obj):
        return obj.item.name


# class CategoryBudgetSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Budget
#         fields = ['item', 'amount',]