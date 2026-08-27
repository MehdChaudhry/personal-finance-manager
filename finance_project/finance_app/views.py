from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, User, Account
from django.db.models import Sum, Func
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import json
from .forms import RegisterForm, CustomLoginForm, CustomPasswordChangeForm, CustomUserChangeForm, TransactionForm, AccountForm, TransferForm
from .models import Budget
from .forms import BudgetForm, BudgetCategoryFormSet
from .forms import BudgetForm
from .forms import TaskForm
from .models import Task
from django.shortcuts import redirect


class Month(Func):
    function = 'TO_CHAR'
    template = "%(function)s(%(expressions)s, 'YYYY-MM')"

@login_required
def dashboard(request):

    transactions = Transaction.objects.filter(user=request.user)

   
    
    # Fetch tasks for the logged-in user
    tasks = Task.objects.filter(user=request.user)
    context = {'tasks': tasks}

    # Fetch tasks that are due soon (within 24 hours)
    from datetime import timedelta
    from django.utils import timezone
    due_soon = tasks.filter(due_date__lte=timezone.now() + timedelta(days=1), due_date__gte=timezone.now())

    # Data for visualizations (as before)
    category_data = transactions.filter(transaction_type='Expense').values('category').annotate(total=Sum('value'))
    monthly_data = transactions.filter(transaction_type='Expense').annotate(month=Month('date')).values('month').annotate(total=Sum('value'))
    income_data = transactions.filter(transaction_type='Income').annotate(month=Month('date')).values('month').annotate(total=Sum('value'))

    # Convert Decimal objects to floats
    category_data = list(category_data)
    for item in category_data:
        item['total'] = float(item['total'])

    monthly_data = list(monthly_data)
    for item in monthly_data:
        item['total'] = float(item['total'])

    income_data = list(income_data)
    for item in income_data:
        item['total'] = float(item['total'])

    # Calculate total spent and deposited
    total_spent = transactions.filter(transaction_type='Expense').aggregate(total=Sum('value'))['total'] or 0
    total_deposited = transactions.filter(transaction_type='Income').aggregate(total=Sum('value'))['total'] or 0

    accounts = Account.objects.filter(user=request.user)
    selected_account_id = request.GET.get('account', None)

    if selected_account_id:
        selected_account = get_object_or_404(Account, id=selected_account_id, user=request.user)
    elif accounts.count() == 1:
        selected_account = accounts.first()
    else:
        selected_account = None

    if selected_account:
        transactions = Transaction.objects.filter(account=selected_account)
        
        # Data for visualizations
        category_data = transactions.filter(transaction_type='Expense').values('category').annotate(total=Sum('value'))
        monthly_data = transactions.filter(transaction_type='Expense').annotate(month=Month('date')).values('month').annotate(total=Sum('value'))
        income_data = transactions.filter(transaction_type='Income').annotate(month=Month('date')).values('month').annotate(total=Sum('value'))

        # Convert Decimal objects to floats
        category_data = list(category_data)
        for item in category_data:
            item['total'] = float(item['total'])

        monthly_data = list(monthly_data)
        for item in monthly_data:
            item['total'] = float(item['total'])

        income_data = list(income_data)
        for item in income_data:
            item['total'] = float(item['total'])

        # Calculate total spent and deposited
        total_spent = transactions.filter(transaction_type='Expense').aggregate(total=Sum('value'))['total'] or 0
        total_deposited = transactions.filter(transaction_type='Income').aggregate(total=Sum('value'))['total'] or 0

        # Calculate current balance
        current_balance = total_deposited - total_spent
    else:
        transactions = []
        category_data = []
        monthly_data = []
        income_data = []
        total_spent = 0
        total_deposited = 0
        current_balance = 0

    # Budget data for bar graph
    budgets = Budget.objects.filter(user=request.user)
    budget_data = []
    for budget in budgets:
        categories = budget.categories.all()
        for category in categories:
            spent = Transaction.objects.filter(user=request.user, category=category.category, transaction_type='Expense').aggregate(total=Sum('value'))['total'] or 0
            budget_data.append({
                'category': category.category,
                'amount': float(category.amount),
                'spent': float(spent)
            })

    # Category icons or emojis
    category_icons = {
        'Food': '🍔',
        'Transport': '🚗',
        'Entertainment': '🎬',
        'Utilities': '💡',
        'Other': '🔧'
    }

    context = {
        'accounts': accounts,
        'selected_account': selected_account,
        'transactions': transactions,
        'tasks': tasks,
        'due_soon': due_soon,
        'category_data': json.dumps(category_data),
        'monthly_data': json.dumps(monthly_data),
        'income_data': json.dumps(income_data),
        'total_spent': total_spent,
        'total_deposited': total_deposited,
        'current_balance': current_balance,
        'budget_data': json.dumps(budget_data),
        'budgets': budgets,
        'category_icons': category_icons,
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        transaction_form = TransactionForm()

    context = {
        'transaction_form': transaction_form,
    }
    return render(request, 'add_transaction.html', context)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a home page or dashboard
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a home page or dashboard
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'password_form': password_form
    })

@login_required
def all_transactions(request):
    filter_option = request.GET.get('filter', 'all')
    transactions = Transaction.objects.filter(user=request.user)

    if filter_option == 'last_day':
        transactions = transactions.filter(date__gte=timezone.now() - timedelta(days=1))
    elif filter_option == 'last_7_days':
        transactions = transactions.filter(date__gte=timezone.now() - timedelta(days=7))
    elif filter_option == 'last_30_days':
        transactions = transactions.filter(date__gte=timezone.now() - timedelta(days=30))

    context = {
        'transactions': transactions,
        'filter_option': filter_option,
    }
    return render(request, 'all_transactions.html', context)

@login_required
def totals_by_category(request):
    totals_by_category = (
        Transaction.objects
        .filter(user=request.user)
        .values('category')
        .annotate(total_amount=Sum('value')) 
        .order_by('category')
    )
    
    context = {
        'totals_by_category': totals_by_category,
    }
    
    return render(request, 'totals_by_category.html', context)

@login_required
def view_transactions_for_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = Transaction.objects.filter(account=account)

    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'view_transactions.html', context)

@login_required
def view_accounts(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'view_accounts.html', {'accounts': accounts})

@login_required
def view_account_details(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)
    transactions = account.transactions.all()

    if request.method == "POST":
        if 'delete' in request.POST:
            account.delete()
            messages.success(request, "Account deleted successfully.")
            return redirect('view_accounts')

    context = {
        'account': account,
        'transactions': transactions,
    }
    return render(request, 'account_details.html', context)

@login_required
def add_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_type = account_form.cleaned_data['account_type']
            if Account.objects.filter(user=request.user, account_type=account_type).exists():
                messages.error(request, f"You already have a {account_type} account.")
            else:
                account = account_form.save(commit=False)
                account.user = request.user
                account.save()

                # Create an initial deposit transaction
                initial_deposit = Transaction(
                    user=request.user,
                    account=account,
                    value=account.balance,
                    category='Income',
                    description='Initial deposit',
                    date=timezone.now().date(),
                    transaction_type='Income'
                )
                initial_deposit.save()

                messages.success(request, 'Account added successfully!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        account_form = AccountForm()

    context = {
        'account_form': account_form,
    }
    return render(request, 'add_account.html', context)

@login_required
def delete_account(request, account_id):
    account = get_object_or_404(Account, id=account_id, user=request.user)

    if request.method == 'POST':
        account.delete()
        messages.success(request, "Account deleted successfully.")
        return redirect('dashboard')
   
    return redirect('dashboard')

@login_required
def create_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        formset = BudgetCategoryFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            formset.instance = budget
            formset.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = BudgetForm()
        formset = BudgetCategoryFormSet()

    return render(request, 'create_budget.html', {'form': form, 'formset': formset})

@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        formset = BudgetCategoryFormSet(request.POST, instance=budget)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = BudgetForm(instance=budget)
        formset = BudgetCategoryFormSet(instance=budget)

    return render(request, 'edit_budget.html', {'form': form, 'formset': formset})

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == "POST":
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('dashboard')
    return render(request, 'delete_budget.html', {'budget': budget})


@login_required
def view_budgets(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'view_budgets.html', {'budgets': budgets})

@login_required
def compare_budgets(request):
    budgets = Budget.objects.filter(user=request.user).order_by('-start_date')[:5]
    if budgets.count() < 2:
        messages.error(request, 'You need at least two budgets to compare.')
        return redirect('dashboard')

    budget_data = []
    for budget in budgets:
        spent = Transaction.objects.filter(user=request.user, budget=budget, transaction_type='Expense').aggregate(total=Sum('value'))['total'] or 0
        budget_data.append({
            'name': budget.name,
            'amount': float(budget.amount),
            'spent': float(spent)
        })

    context = {
        'budget_data': json.dumps(budget_data),
    }
    return render(request, 'compare_budgets.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            task.save()
            messages.success(request, 'Task added successfully!')
            return redirect('dashboard')  # Redirect to the dashboard after task creation
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        task_form = TaskForm()

    context = {
        'task_form': task_form,
    }
    return render(request, 'add_task.html', context)




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task

@login_required
def create_or_edit_task(request, task_id=None):
    if task_id:
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task_form = TaskForm(request.POST or None, instance=task)
    else:
        task = None
        task_form = TaskForm(request.POST or None)
    
    if request.method == 'POST':
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.user = request.user  # Ensure task is assigned to the logged-in user
            task.save()
            messages.success(request, 'Task saved successfully!')
            return redirect('dashboard')
    
    return render(request, 'create_task.html', {'task_form': task_form, 'task': task})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure task belongs to the logged-in user

    if request.method == 'POST':
        task.delete()  # Delete the task
        messages.success(request, 'Task deleted successfully!')
        return redirect('dashboard')  # Redirect after deletion
    
    return redirect('dashboard')  # Redirect if it's a GET request

def transfer_funds(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account = form.cleaned_data['from_account']
            to_account = form.cleaned_data['to_account']
            amount = form.cleaned_data['amount']

            if from_account.balance < amount:
                messages.error(request, "Insufficient funds in the from account.")
                return redirect('transfer_funds')

            if from_account == to_account:
                messages.error(request, "You cannot transfer money to the same account.")
                return redirect('transfer_funds')

            from_account.balance -= amount 
            to_account.balance += amount  

            from_account.save()
            to_account.save()

            Transaction.objects.create(
                user=request.user,
                account=from_account,
                value=-amount,
                category="Transfer",
                description=f"Transferred {amount} to {to_account.account_type}",
                date=timezone.now().date(),
                transaction_type="Expense"
            )

            Transaction.objects.create(
                user=request.user,
                account=to_account,
                value=amount,
                category="Transfer",
                description=f"Received {amount} from {from_account.account_type}",
                date=timezone.now().date(),
                transaction_type="Income"
            )

            messages.success(request, f"Successfully transferred {amount} from {from_account} to {to_account}.")
            return redirect('dashboard')
    else:
        form = TransferForm()

    return render(request, 'transfer_funds.html', {'form': form})






