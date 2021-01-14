from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class CustomUserForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Password'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'fullname', 'phone','tanggal_lahir', 'status',)
        labels = {
            'phone': 'Phone (WhatsApp)'
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email' , 'style':"text-transform: lowercase;"}),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fullname'}),
            'institusi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institusi'}),
            'domisili': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domisili'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'onkeypress':'return event.charCode >= 48', 'min':'1'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'fullname', 'phone','tanggal_lahir', 'status', )
        labels = {
            'phone': 'Phone (WhatsApp)'
        }

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'readonly':True}),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fullname'}),
            'institusi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Institusi'}),
            'domisili': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Domisili'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (With Country Code)', 'onkeydown': 'javascript: return event.keyCode == 69 ? false : true', }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),
            'is_marketing_squard': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

