import locale

from django.db.models import Sum
from django.contrib.auth import get_user_model


from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Item, Category, Transaction, Budget, Goal

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    """Custom login serializer"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def get_token(self, user):
        refresh_token = RefreshToken.for_user(user)
        access = str(refresh_token.access_token)
        refresh = str(refresh_token)
        return access, refresh

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = User.objects.get(email=email)
        request = self.context.get('request')
        
        if not user or not user.check_password(password):
            credentials = {'email': email}
            raise serializers.ValidationError('Invalid login credentials or not a verified user')
        
        access, refresh = self.get_token(user)
        
        payload = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': email,
            'access': access,
            'refresh': refresh,
        }
        return payload


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ['id', 'name', 'category']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', ]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'item', 'amount', 'date', 'category_name', 'item_name', 'time']

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
        fields = ['id', 'name', 'target_amount', 'target_savings', 'saved', 'progress', 'target_date']

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
        fields = ['id', 'item', 'amount', 'month', 'spent', 'category_name', 'item_name']

    def get_spent(self, obj) -> int:
        spent_amount = Transaction.objects.filter(date__month=obj.month, item=obj.item).aggregate(total_amount=Sum('amount'))
        return spent_amount['total_amount']
    
    def get_category_name(self, obj) -> str:
        return obj.item.category.name

    def get_item_name(self, obj) -> str:
        return obj.item.name


# class CategoryBudgetSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Budget
#         fields = ['item', 'amount',]