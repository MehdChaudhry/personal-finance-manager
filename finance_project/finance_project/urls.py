"""
URL configuration for finance_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from finance_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('all_transactions/', views.all_transactions, name='all_transactions'),  
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('accounts/<int:account_id>/transactions/', views.view_transactions_for_account, name='view_transactions'),
    path('account/<int:account_id>/', views.view_account_details, name='view_account_details'),
    path('delete_account/<int:account_id>/', views.delete_account, name='delete_account'),
    path('add_account/', views.add_account, name='add_account'),
    path('view_accounts/', views.view_accounts, name='view_accounts'),
    path('totals/', views.totals_by_category, name='totals_by_category'),
    path('create_budget/', views.create_budget, name='create_budget'),
    path('budgets/', views.view_budgets, name='view_budgets'),
    path('edit_budget/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('delete_budget/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_task/', views.add_task, name='add_task'),
    path('task/create/', views.create_or_edit_task, name='create_task'),
    path('task/<int:task_id>/edit/', views.create_or_edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),  # Keep the delete task URL here
    path('transfer_funds/', views.transfer_funds, name='transfer_funds'),
]

    


