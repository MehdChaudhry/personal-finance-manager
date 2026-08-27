from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Transaction, Budget, Account, BudgetCategory
from .models import Transaction, Budget, Account
from django import forms
from .models import Task


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=200)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CustomUserChangeForm(UserChangeForm):
    password = None  # Exclude the password field

    class Meta:
        model = User
        fields = ['username', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'value', 'category', 'description', 'transaction_type', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['account_type', 'balance']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = []
        

class BudgetCategoryForm(forms.ModelForm):
    class Meta:
        model = BudgetCategory
        fields = ['category', 'amount']

BudgetCategoryFormSet = forms.inlineformset_factory(Budget, BudgetCategory, form=BudgetCategoryForm, extra=1)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'is_completed'] 
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'month': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_month(self):
        month = self.cleaned_data['month']
        return month.replace(day=1)  

class TransferForm(forms.Form):
    from_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="From Account")
    to_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="To Account")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Amount to Transfer")

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount