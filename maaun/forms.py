from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from .models import Election,Position, Candidate, Voter




# Registration form
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

# Login form
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['year']


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'election']

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'department', 'reg_no', 'position', 'avater']

class updteCandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'department', 'reg_no',  'avater']

class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = ["first_name", "last_name", "department", "reg_no", "level"]

    def save(self, commit=True):
        voter = super().save(commit=False)
        voter.set_password(voter.reg_no)  # 🔴 Ensure password is hashed
        if commit:
            voter.save()
        return voter



class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if new != confirm:
            raise forms.ValidationError("New passwords do not match")
        return cleaned_data