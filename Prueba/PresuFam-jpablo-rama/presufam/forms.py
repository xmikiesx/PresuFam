from django import forms
from .models import MyUser, Income, Category, Expense
from django.contrib.auth.forms import UserChangeForm


class DateInput(forms.DateInput):
    input_type = 'date'


class MyUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ['nombre', 'apellido', 'email', 'password']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')

        t = False
        for c in email:
            if c == '@':
                t = True

        if t:
            email_base, provider = email.split('@')
            if not provider == 'presufam.com':
                raise forms.ValidationError("Porfavor asegurate de usar un email @presufam.com.")
            return email
        else:
            raise forms.ValidationError("Necesitas ingresar @presufam.com!!")


class MyUserUpdateForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['nombre', 'apellido', 'password']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class SignInForm(forms.Form):
    email = forms.CharField(required=True, label='Email',
                            widget=(forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'})))
    password = forms.CharField(required=True, label='Password',
                               widget=(forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})))


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['nombre', 'monto', 'fecha', 'categoria']

        # The fields present in the form
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Category.objects.filter(user=user)


class IncomeUpdateForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['nombre', 'monto', 'fecha']

        # The fields present in the form
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': DateInput(attrs={'class': 'form-control'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['nombre', 'monto', 'fecha', 'categoria']

        # The fields present in the form
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Category.objects.filter(user=user)


class ExpenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['nombre', 'monto', 'fecha']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': DateInput(attrs={'class': 'form-control'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['nombre']

        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }