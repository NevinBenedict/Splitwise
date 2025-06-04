from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Group, GroupMember
from user_app.models import User
from .serializers import GroupSerializer, GroupMemberSerializer
from django.shortcuts import get_object_or_404

class GroupListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = Group.objects.filter(members=request.user)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save(created_by=request.user)
            group.members.add(request.user)
            members = request.data.get('members', [])
            if members:
                group.members.add(*members)
            return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Group, pk=pk)

    def get(self, request, pk):
        group = self.get_object(pk)
        if request.user not in group.members.all():
            return Response({'detail': 'Not a member of this group.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk):
        group = self.get_object(pk)
        if request.user != group.created_by:
            return Response({'detail': 'Only creator can update.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        if request.user != group.created_by:
            return Response({'detail': 'Only creator can delete.'}, status=status.HTTP_403_FORBIDDEN)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupMemberAddAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        if request.user != group.created_by:
            return Response({'detail': 'Only creator can add members.'}, status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        group.members.add(user)
        return Response({'detail': 'Member added.'}, status=status.HTTP_200_OK)

class GroupMemberDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, uk):
        group = get_object_or_404(Group, pk=pk)
        user = get_object_or_404(User, pk=uk)
        if request.user != group.created_by and request.user != user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        group.members.remove(user)
        return Response({'detail': 'Member removed.'}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from expenseapp.models import Expense, ExpenseSplit, Settlement
from user_app.models import User
from group.models import *
from .serializers import ExpenseSerializer, ExpenseSplitSerializer, SettlementSerializer
from django.shortcuts import get_object_or_404
from decimal import Decimal

class ExpenseListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id=None):
        if group_id:
            expenses = Expense.objects.filter(group_id=group_id)
        else:
            expenses = Expense.objects.filter(group__members=request.user)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)

    def post(self, request, group_id=None):
        group = get_object_or_404(Group, id=group_id)
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            expense = serializer.save(paid_by=request.user, group=group)
            return Response(ExpenseSerializer(expense).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExpenseDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def put(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        if expense.paid_by != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ExpenseSerializer(expense, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk)
        if expense.paid_by != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExpenseSplitAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, expense_id):
        splits = ExpenseSplit.objects.filter(expense_id=expense_id)
        serializer = ExpenseSplitSerializer(splits, many=True)
        return Response(serializer.data)

    def post(self, request, expense_id):
        expense = get_object_or_404(Expense, id=expense_id)
        if expense.paid_by != request.user:
            return Response({'detail': 'Not allowed.'}, status=status.HTTP_403_FORBIDDEN)
        # You need to implement the split logic here based on split_type and request.data
        # For now, just a placeholder
        return Response({'detail': 'Split logic not implemented.'}, status=status.HTTP_501_NOT_IMPLEMENTED)

class SettlementListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id=None):
        if group_id:
            settlements = Settlement.objects.filter(payer=request.user, expense__group_id=group_id)
        else:
            settlements = Settlement.objects.filter(payer=request.user)
        serializer = SettlementSerializer(settlements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SettlementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(payer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PendingExpenseAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expensesplit = ExpenseSplit.objects.filter(user=request.user, balance__gt=0)
        serializer = ExpenseSplitSerializer(expensesplit, many=True)
        return Response(serializer.data)

class LentSplitAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = ExpenseSplit.objects.filter(expense__paid_by=request.user.id, balance__gt=0)
        serializer = ExpenseSplitSerializer(data, many=True)
        return Response(serializer.data)