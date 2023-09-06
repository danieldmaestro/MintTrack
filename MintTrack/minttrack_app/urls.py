from django.urls import path
from . import views

app_name = 'minttrack_app'

urlpatterns = [
    path('transactions/', views.TransactionListAPIView.as_view(), name="transactions"),
    path('transaction/create/', views.TransactionCreateAPIView.as_view(), name="transaction_create"),
    path("budgets/", views.BudgetListAPIView.as_view(), name="budget_list"),
    path("budget/create/", views.BudgetCreateAPIView.as_view(), name="budget_create"),
    path("goals/", views.GoalListAPIView.as_view(), name="goal_list"),
    path("goals/create/", views.GoalCreateAPIView.as_view(), name="goal_create"),
]

