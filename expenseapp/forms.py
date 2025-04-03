from django import forms
from .models import *

class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'total_amount','split_type']