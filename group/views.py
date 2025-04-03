from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from .models import Group, GroupMember
from user_app.models import User
from django.urls import reverse_lazy
from expenseapp.models import *
from .forms import GroupCreateForm, GroupMemberForm
from django.utils.decorators import method_decorator

def login_user(fn):
    def wrapper(request,**kwargs):
        if request.user.is_authenticated:
            return fn(request,**kwargs)
        else:
            return redirect('logout')
    return wrapper

@method_decorator(login_user,name="dispatch")
class GroupCreateView(CreateView):
    def get(self, request):
        form = GroupCreateForm()
        form.fields["users"].queryset = User.objects.exclude(id=request.user.id)
        return render(request, 'group_create_form.html', {'form': form})

    def post(self, request):
        form = GroupCreateForm(request.POST)
        form.fields["users"].queryset = User.objects.exclude(id=request.user.id)
        if form.is_valid():
            # Create the group with the logged-in user as the creator
            group = Group.objects.create(name=form.cleaned_data.get('name'), created_by=request.user)
            group.members.add(request.user)  # Add the creator to the group

            # Add additional members to the group
            users = form.cleaned_data.get('users')  # Use 'users' field for multiple members
            if users:
                group.members.add(*users)  # Add all selected users to the group

            return redirect('group_list')
        return render(request, 'group_create_form.html', {'form': form})


class GroupListView(ListView):
    model = Group
    template_name = 'group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(members=self.request.user)
        return queryset


class GroupDetailView(View):
    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        data=ExpenseSplit.objects.filter(expense__group=pk, user=request.user)
        if request.user in group.members.all():

            return render(request, 'group_detail.html', {'group': group, 'data':data})
        return redirect('group_list')

class GroupUpdateView(UpdateView):
    model = Group
    fields = ['name']
    template_name = 'group_update_form.html'
    success_url = reverse_lazy('group_list')


class GroupDeleteView(View):
    def post(self, request, pk):
        data=ExpenseSplit.objects.filter(expense__group=pk)
        if data.exists():
            for i in data:

                        if i.balance>0:
                            return redirect('group_detail', pk=group.id)

        group = Group.objects.get(id=pk)
        if request.user == group.created_by:
            group.delete()
            return redirect('group_list')
        return redirect('login')
    

    


class GroupMemberAddView(View):
    template_name = 'group_member_add.html'  # Replace with your template name

    def get(self, request, pk):
        group = Group.objects.get(id=pk)
        form = GroupMemberForm(group=group)  # Pass group as a keyword argument
        return render(request, self.template_name, {'form': form, 'group': group})

    def post(self, request, pk):
        group = Group.objects.get(id=pk)
        form = GroupMemberForm(request.POST, group=group)  # Pass group to form

        if request.user == group.created_by:
            if form.is_valid():
                # Save the GroupMember instance
                user = form.cleaned_data['user']
                group.members.add(user)
                
                return redirect('group_list')
            # If form is invalid, re-render with errors
            return render(request, self.template_name, {'form': form, 'group': group})
        # If user is not the creator, redirect to login (or handle differently)
        return redirect('login')


class GroupMemberDeleteView(View):
    

    def post(self, request, pk, uk):
        try:
            group = Group.objects.get(id=pk)
            user = User.objects.get(id=uk)

            
            if request.user == group.created_by or request.user == user:

                data=ExpenseSplit.objects.filter(expense__group=pk)

                if data.exists():
                    
                    for i in data:

                        if i.balance>0:
                            return redirect('group_detail', pk=group.id)
                              


                if group.members.filter(id=user.id).exists():
                        group.members.remove(user)
                        return redirect('group_detail', pk=group.id)
                else:
                        
                    return redirect('group_detail', pk=group.id)
                    
                    
                
            else:
                
                return redirect('group_detail', pk=group.id)

        except Group.DoesNotExist:
           
            return redirect('group_list')
        except User.DoesNotExist:
            
            return redirect('group_detail', pk=group.id)
