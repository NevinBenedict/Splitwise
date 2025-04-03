from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.db.models import Q
from user_app.models import *
from group.models import *
from .forms import *
from django.utils.decorators import method_decorator
from decimal import Decimal
from django.core.mail import send_mail

def login_user(fn):
    def wrapper(request,**kwargs):
        if request.user.is_authenticated:
            return fn(request,**kwargs)
        else:
            return redirect('logout')
    return wrapper
# Create your views here.

class AddExpense(View):
    def get(self, request,**kwargs):
        id = kwargs.get('pk')
        group = Group.objects.get(id=id)
        form = AddExpenseForm()
        
        return render(request, 'add_expense.html', {'form':form,'group': group, 'user': request.user})
    
    def post(self, request,**kwargs):
        id = kwargs.get('pk')
        group = Group.objects.get(id=id)
        user = User.objects.get(id=request.user.id)
        form = AddExpenseForm(request.POST)
        
        if form.is_valid():
            if request.user in group.members.all():
                data=Expense.objects.create(**form.cleaned_data, paid_by=user, group=group)
                
                return redirect('expense_split', pk=data.id)
            
        return redirect('login')
        
class ExpenseList(View):
    def get(self, request,**kwargs):
        id = kwargs.get('pk')
        group = Group.objects.get(id=id)
        expenses = Expense.objects.filter(group=group)
        user=User.objects.get(id= request.user.id)
        
        return render(request, 'expense_list.html', {'expenses':expenses,'group':group,'user':user})
    

class ExpenseDelete(View):
    def get(self, request,**kwargs):
        id = kwargs.get('pk')
        expenses = Expense.objects.get(id=id)
        
        if request.user == expenses.paid_by:
            expenses.delete()
            return redirect('group_list',)
        
        return render('group_list')
    
class ExpenseSplitView(View):
    def get(self, request,**kwargs):
        
        id = kwargs.get('pk')
        
        expenses = Expense.objects.get(id=id)
        members = expenses.group.members.all()
        return render(request, 'expense_split.html', {'i': expenses ,'members':members,})

    
    def post(self, request,**kwargs):
            
            id = kwargs.get('pk')
            
            expenses = Expense.objects.get(id=id)
        
            

            data=ExpenseSplit.objects.filter(expense=id)
            user = User.objects.get(id=request.user.id)
            if user==expenses.paid_by:
                if not data.exists():
                    expenses = Expense.objects.get(id=id)
                    user = User.objects.get(id=request.user.id)
                    if expenses.split_type == 'EQUAL':
                        members = expenses.group.members.all().count()
                        
                        amount_owed = expenses.total_amount / (members-1)
                        for member in expenses.group.members.all():
                            if member != expenses.paid_by:

                                ExpenseSplit.objects.create(expense=expenses, user=member, amount_owed=amount_owed,balance=amount_owed)
                                send_mail(
                                    "Splitwise Notification",
                                    f"hi {member.username},\n You have split of amount {amount_owed} paid to {user.username}.",
                                    "nevinbenedict07@gmail.com",
                                    [member.email],
                                    fail_silently=False
                                )
                    elif expenses.split_type == 'PERCENTAGE':
                        members=expenses.group.members.all()
                        user= User.objects.get(id=request.user.id)
                        s = sum(float(value) for key, value in request.POST.items() if key.startswith('percentage_'))
                        
                        if s!=100:

                            return redirect('expense_split', pk=id)


                        else:    
                            for member in members:


                                if member!= expenses.paid_by:
                                    
                                    percentage = float(request.POST.get(f'percentage_{member.id}',0))
                                    
                                    amount_owed=float(expenses.total_amount)*(percentage/100)
                                    
                                    ExpenseSplit.objects.create(expense=expenses, user=member, amount_owed=amount_owed,percentage=percentage,balance=amount_owed)
                                    send_mail(
                                    "Splitwise Notification",
                                    f"hi {member.username},\n You have split of amount {amount_owed} paid to {user.username}.",
                                    "nevinbenedict07@gmail.com",
                                    [member.email],
                                    fail_silently=False
                                )

                    elif expenses.split_type == 'EXACT':
                        members=expenses.group.members.all()
                        user= User.objects.get(id=request.user.id)
                        s = sum(float(value) for key, value in request.POST.items() if key.startswith('amount_'))
                        
                        if s!=expenses.total_amount:

                            return redirect('expense_split', pk=id)


                        else:    
                            for member in members:


                                if member!= expenses.paid_by:
                                    
                                    amount_owed = float(request.POST.get(f'amount_{member.id}',0))
                                
                                    ExpenseSplit.objects.create(expense=expenses, user=member, amount_owed=amount_owed,balance=amount_owed)

                                    send_mail(
                                                "Splitwise Notification",
                                                f"hi {member.username},\n You have split of amount {amount_owed} paid to {user.username}.",
                                                "nevinbenedict07@gmail.com",
                                                [member.email],
                                                fail_silently=False
                                            )
                else:
                    print('already exists')

            return redirect('group_list')
        
        
    
class ExpenseSplitListView(View):
    def get(self, request,**kwargs):
        id = kwargs.get('pk')
        data=ExpenseSplit.objects.filter(expense__group=id, user=request.user)
        
        return render(request, 'expense_split_list.html', {'data':data,})
    
# Settlement
@method_decorator(login_user, name="dispatch")

class SettlementView(View):
    
    def post(self, request, **kwargs):
        id = kwargs.get('pk')
        print(request.POST)
        data = ExpenseSplit.objects.get(id=id)
        
        if data.user == request.user:
            amount = Decimal(request.POST.get('amount', 0))
            if amount <= 0 or amount > data.balance:
                return redirect('dashboard')
            if data.balance == 0:
                return redirect('dashboard')
            Settlement.objects.create(payer=data.user, payee=data.expense.paid_by, amount= amount, expense=data.expense)
            data.balance -= amount
            data.save()
        return redirect('group_detail',pk=data.expense.group.id)
    

    
class SettlementListView(View):
    def get(self, request,**kwargs):
        id = kwargs.get('pk')
        data=Settlement.objects.filter(payer=request.user, expense__group=id)
        
        return render(request, 'settlement_list.html', {'data':data,})
    
@method_decorator(login_user,name="dispatch")
class DashboardView(View):
    def get(self, request,**kwargs):
        id = kwargs.get('pk')
        group = Group.objects.filter(members=request.user)
        
        user= User.objects.get(id=request.user.id)
        data=Settlement.objects.filter(Q(payer=request.user) | Q(payee=request.user))
        
        expensesplit=ExpenseSplit.objects.filter(user=request.user)
        es=sum(i.balance for i in expensesplit)
        expenses=ExpenseSplit.objects.filter(expense__paid_by= request.user.id)
        e=sum(i.amount_owed for i in expenses)
        return render(request, 'dashboard.html', {'data':data,'group':group,'expenses':expenses,'user':user,'g':group.count(),'e':e,'es':es})

class ExpenseUserListView(View):
    def get(self, request):
       
        data=Expense.objects.filter( group__members=request.user)
        
        return render(request, 'expense_user_list.html', {'expenses':data,})
    
class SettlementUserListView(View):
    def get(self, request):
        
        data=Settlement.objects.filter(payer=request.user)
        
        return render(request, 'settlement_list.html', {'data':data,})


class PendingExpenseView(View):

    def get(self, request):
        expensesplit=ExpenseSplit.objects.filter(user=request.user,balance__gt=0)
        return render(request,"pending_expense.html",{'data':expensesplit})
    

class ExpenseUpdateView(View):

    def get(self,request,pk):

        data=Expense.objects.get(id=pk)

        if data.paid_by!=request.user:

            return redirect('login')

        form=AddExpenseForm(instance=data)

        return render(request,"update_expense.html",{'form':form,'data':data})

        
    def post(self,request,pk):

        data=Expense.objects.get(id=pk)

        form=AddExpenseForm(request.POST,instance=data)

        if form.is_valid():

            expense=ExpenseSplit.objects.filter(expense=data)

            settle= Settlement.objects.filter(expense=data)

            if expense and not settle:

                expense.delete()

                form.save()
            else:
                print("already closed")

                return redirect('group_list')

        return redirect('expense_split', pk=data.id)
            

class LentSplitView(View):
    
    def get(self,request):
    
        data=ExpenseSplit.objects.filter(expense__paid_by= request.user.id, expense__gt=0)

        return render(request, 'expense_split_list.html', {'data':data,})


class ExpenseDelete(View):

    def get (self,request,pk):

        data = Expense.objects.get(id=pk)

        split=ExpenseSplit.objects.filter(expense=data)

        for i in split:

            if i.balance>0 and i.balance!=i.amount_owed:

                return redirect('dashboard')
            
        data.delete()
        # split.delete()

        return redirect ('group_list')


class Notifymail(View):
    def get(self,request,pk):
        data=ExpenseSplit.objects.get(id=pk)
        user=User.objects.get(id=request.user.id)
        send_mail(
                    "Splitwise Notification",
                    f"hi {data.user.username},\n You have split of amount {data.balance} paid to {user.username}.",
                    "nevinbenedict07@gmail.com",
                    [data.user.email],
                    fail_silently=False
                                            )
        return redirect('lent_expense')
        



        

