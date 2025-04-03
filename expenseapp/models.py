from django.db import models
from user_app.models import *
from group.models import *
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Expense(models.Model):
    SPLIT_TYPES = (
        ('EQUAL', 'Equal'),
        ('EXACT', 'Exact'),
        ('PERCENTAGE', 'Percentage'),
    )

    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    paid_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='expenses_paid')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, related_name='expenses')
    split_type = models.CharField(max_length=10, choices=SPLIT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} ({self.total_amount})"

class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_splits')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],default=0)
    
    def __str__(self):
        return f"{self.user.username} owes {self.amount_owed} for {self.expense}"
    

class Settlement(models.Model):
    payer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='settlements_made')
    payee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='settlements_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, null=True, blank=True, related_name='settlements')
    settled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payer.username} paid {self.payee.username} {self.amount}"