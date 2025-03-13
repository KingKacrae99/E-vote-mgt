from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from voteapp.models import *

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'email', 'phone', 'is_admin']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if len(phone) > 15:
            raise forms.ValidationError("Phone number must not be more the 15 digits.")
        return phone

    def save(self, commit=True):
            member = super().save(commit=False)
            if commit:
                member.save()
            return member
    
class PositionForm(forms.ModelForm):
     class Meta:
          model = Position
          fields = ['title', 'descript']
          widgets={
               'title':forms.TextInput(attrs={'class': 'form-control'}),
               'descript':forms.TextInput(attrs={'class': 'form-control'}),
          }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'position', 'profile_pic', 'profile']
        widgets={
             'name':forms.TextInput(attrs={'class': 'form-control'}),
             'position': forms.Select(attrs={'class': 'form-control'}),
             'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control custom-border'}),
             'profile': forms.TextInput(attrs={'class':'form-control custom-border', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a placeholder option to the position field
        self.fields['position'].empty_label = "Select Position"
