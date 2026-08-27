from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('Checking', 'Checking'),
        ('Savings', 'Savings'),
        ('Credit', 'Credit'),
        ('Investment', 'Investment'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_type} - {self.user.username}"

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other'),
    ]
    TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=100)
    date = models.DateField()
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.category} - {self.value}"
    
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')

    def __str__(self):
        return f"Budget for the user {self.user.username}"

class BudgetCategory(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')
    category = models.CharField(max_length=50, choices=Transaction.CATEGORY_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Task(models.Model):
    name = models.CharField(max_length=255)  # Add a name field
    description = models.TextField()
    due_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Task: {self.name} (due on {self.due_date})"

