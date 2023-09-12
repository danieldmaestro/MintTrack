from django.db.models import Sum

from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import Item, Category, Transaction, Budget, Goal, GoalTransaction
from .serializers import ItemSerializer, CategorySerializer, ItemBudgetSerializer, TransactionSerializer, GoalSerializer, LoginSerializer



# Create your views here.

class LoginAPIView(TokenObtainPairView):
    """Endpoint to get authenticate user"""
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    
class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class TransactionCreateAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()


class BudgetListAPIView(generics.ListAPIView):
    serializer_class = ItemBudgetSerializer
    queryset = Budget.objects.all()


class BudgetCreateAPIView(generics.CreateAPIView):
    serializer_class = ItemBudgetSerializer
    queryset = Budget.objects.all()

    def perform_create(self, serializer):
        return super().perform_create(serializer)
    

class GoalListAPIView(generics.ListAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()


class GoalCreateAPIView(generics.CreateAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def perform_create(self, serializer):
        return super().perform_create(serializer)
    

class BudgetDataAPIView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        total_balance = Budget.objects.all().aggregate(total=Sum('amount'))['total']
        total_spent = Transaction.objects.all().aggregate(total=Sum('amount'))['total']
        total_saved = GoalTransaction.objects.all().aggregate(total=Sum('amount'))['total']
        message = {
            'total_balance': total_balance,
            'total_spent': total_spent,
            'total_saved': total_saved
                   }
        return Response(message, status=status.HTTP_200_OK)
    




