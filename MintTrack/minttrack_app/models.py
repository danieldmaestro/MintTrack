import math

from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    time = models.TimeField(auto_now=True)
    date = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-time']

    def __str__(self) -> str:
        return f'{self.item.name} - {self.amount}'
  

class Goal(models.Model):
    name = models.CharField(max_length=100)
    target_amount = models.PositiveIntegerField()
    target_savings = models.PositiveIntegerField()
    start_date = models.DateField(auto_now=True)
    target_date = models.DateField(validators=[MinValueValidator(limit_value=timezone.now().date())])

    def __str__(self) -> str:
        return f"Goal: {self.name}, Amount: {self.target_amount}"
    
    def saved(self):
        saved = self.goal_transactions.all().aggregate(total=models.Sum('amount'))['total']
        if saved:
            return saved
        return 0
    
    def progress(self):
        return math.ceil((self.saved() / self.target_amount) * 100)


class GoalTransaction(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="goal_transactions")
    amount = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f'Saved {self.amount} towards {self.goal.name}'


class Budget(models.Model):
    MONTH_CHOICES = (
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    # spent = models.PositiveIntegerField()
    month = models.IntegerField(choices=MONTH_CHOICES, null=True)

    class Meta:
        unique_together = ('item', 'month')

    def __str__(self):
        return f"Budget for {self.item.name} for {self.month}"
