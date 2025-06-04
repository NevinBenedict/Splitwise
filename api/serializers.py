from rest_framework import serializers
from group.models import Group, GroupMember
from user_app.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'user', 'joined_at']

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'created_by', 'created_at', 'members']


from rest_framework import serializers
from expenseapp.models import Expense, ExpenseSplit, Settlement
from user_app.models import User
from group.models import Group

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class ExpenseSplitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ExpenseSplit
        fields = ['id', 'expense', 'user', 'amount_owed', 'percentage', 'balance']

class ExpenseSerializer(serializers.ModelSerializer):
    paid_by = UserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    splits = ExpenseSplitSerializer(many=True, read_only=True)

    class Meta:
        model = Expense
        fields = [
            'id', 'description', 'total_amount', 'paid_by', 'group',
            'split_type', 'created_at', 'splits'
        ]

class SettlementSerializer(serializers.ModelSerializer):
    payer = UserSerializer(read_only=True)
    payee = UserSerializer(read_only=True)
    expense = ExpenseSerializer(read_only=True)

    class Meta:
        model = Settlement
        fields = ['id', 'payer', 'payee', 'amount', 'expense', 'settled_at']