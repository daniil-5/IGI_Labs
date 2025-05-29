from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Customer


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'
    }))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))

    class Meta:
        model = User
        fields = ('username', 'password', 'remember_me')


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Выберите имя пользователя'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+375 (XX) XXX-XX-XX',
        'data-mask': '+375 (00) 000-00-00'
    }))

    # Define min_date for birth date (18 years ago from today)
    min_date = timezone.now().date().replace(year=timezone.now().year - 100)
    max_date = timezone.now().date().replace(year=timezone.now().year - 18)

    # Fixed birth_date field with proper date range
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': min_date.isoformat(),
            'max': max_date.isoformat(),
            'value': max_date.isoformat()  # default 18 years ago
        }),
        input_formats=['%Y-%m-%d', '%d/%m/%Y']  # Accept both ISO and DD/MM/YYYY formats
    )

    terms_agreement = forms.BooleanField(required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Check if the phone number matches the required format
        import re
        if not re.match(r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            raise ValidationError('Номер телефона должен быть в формате: +375 (XX) XXX-XX-XX')
        return phone_number

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = timezone.now().date()

        if birth_date is None:
            raise ValidationError('Дата рождения обязательна')

        if birth_date > today:
            raise ValidationError('Дата рождения не может быть в будущем')

        # Calculate age
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        if age < 18:
            raise ValidationError('Вам должно быть не менее 18 лет')

        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Create the Customer profile
            Customer.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number'],
                birth_date=self.cleaned_data['birth_date']
            )

        return user