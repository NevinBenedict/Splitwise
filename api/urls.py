from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    
    TokenRefreshView,
)
from .views import *

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('groups/', GroupListCreateAPIView.as_view(), name='group-list-create'),
    path('groups/<int:pk>/', GroupDetailAPIView.as_view(), name='group-detail'),
    path('groups/<int:pk>/add-member/', GroupMemberAddAPIView.as_view(), name='group-add-member'),
    path('groups/<int:pk>/remove-member/<int:uk>/', GroupMemberDeleteAPIView.as_view(), name='group-remove-member'),
    path('expenses/', ExpenseListCreateAPIView.as_view(), name='expense-list-create'),
    path('expenses/group/<int:group_id>/', ExpenseListCreateAPIView.as_view(), name='expense-list-create-group'),
    path('expenses/<int:pk>/', ExpenseDetailAPIView.as_view(), name='expense-detail'),
    path('expenses/<int:expense_id>/splits/', ExpenseSplitAPIView.as_view(), name='expense-split'),
    path('settlements/', SettlementListCreateAPIView.as_view(), name='settlement-list-create'),
    path('settlements/group/<int:group_id>/', SettlementListCreateAPIView.as_view(), name='settlement-list-group'),
    path('expenses/pending/', PendingExpenseAPIView.as_view(), name='pending-expense'),
    path('expenses/lent/', LentSplitAPIView.as_view(), name='lent-expense'),
]
