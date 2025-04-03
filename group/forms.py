from django import forms
from user_app.models import User
from .models import *

class GroupCreateForm(forms.Form):

    name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # Populate with all users
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    

class GroupMemberForm(forms.ModelForm):
    def __init__(self, *args, group=None, **kwargs):
        super().__init__(*args, **kwargs)
        if group:
            # Exclude users who are already members of the group
            existing_members = group.members.all().values_list('id', flat=True)
            self.fields['user'].queryset = User.objects.exclude(id__in=existing_members)

    user = forms.ModelChoiceField(
        queryset=User.objects.all(),  # Initial queryset, will be filtered in __init__
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select a user"
    )

    class Meta:
        model = GroupMember
        fields = ['user']

    

