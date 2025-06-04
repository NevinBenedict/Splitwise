"""
URL configuration for splitwise project.

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
from django.urls import path,include
from user_app.views import *
from group.views import *
from expenseapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',Registeration.as_view(),name='register'),
    path('otp/',Otpverification.as_view(),name='otp'),
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('userprofile/',UserProfileView.as_view(),name='userprofile'),
    path('userupdate/',UserUpdate.as_view(),name='userupdate'),
    path('group/creategroup/',GroupCreateView.as_view(),name='creategroup'),
    path('group/list/',GroupListView.as_view(),name='group_list'),
    path('group/detail/<int:pk>/',GroupDetailView.as_view(),name='group_detail'),
    path('group/delete/<int:pk>/',GroupDeleteView.as_view(),name='group_delete'),
    path('group/update/<int:pk>/',GroupUpdateView.as_view(),name='group_update'),
    path('group/addmember/<int:pk>/',GroupMemberAddView.as_view(),name='addmember'),
    path('group/deletemember/<int:pk>/<int:uk>',GroupMemberDeleteView.as_view(),name='delete_member'),
    path('expense/addexpense/<int:pk>/',AddExpense.as_view(),name='add_expense'),
    path('expense/updateexpense/<int:pk>/',ExpenseUpdateView.as_view(),name='update_expense'),
    path('expense/listexpense/<int:pk>/',ExpenseList.as_view(),name='expense_list'),
    path('expense/deleteexpense/<int:pk>/',ExpenseDelete.as_view(),name='expense_delete'),
    path('expense/split/<int:pk>/',ExpenseSplitView.as_view(),name='expense_split'),
    path('expense/splitlist/<int:pk>/',ExpenseSplitListView.as_view(),name='expense_split_list'),
    path('expense/settlement/<int:pk>/',SettlementView.as_view(),name='settlement'),
    path('expense/settlementlist/<int:pk>/',SettlementListView.as_view(),name='settlement_list'),
    path('Dashboard/',DashboardView.as_view(),name='dashboard'),
    path('expense/expensesuserlist/',ExpenseUserListView.as_view(),name='expense_user_list'),
    path('expense/pendingexpense/',PendingExpenseView.as_view(),name='pending_expense'),
    path('expense/settlementuserlist/',SettlementUserListView.as_view(),name='settlement_user_list'),
    path('expense/lentexpense/',LentSplitView.as_view(),name='lent_expense'),
    path('expense/delete/<int:pk>',ExpenseDelete.as_view(),name='delete_expense'),
    path('expense/notifymail/<int:pk>/',Notifymail.as_view(),name='notify_mail'),
    path('api/',include('api.urls'))
    

]
