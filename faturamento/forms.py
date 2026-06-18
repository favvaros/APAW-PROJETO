# ARQUIVO: faturamento/forms.py
# Crie este arquivo em faturamento/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Fatura
import re


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nome de usuário'})
        self.fields['username'].label = 'Usuário'
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita a senha'})
        self.fields['password2'].label = 'Confirmar Senha'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'cpf_cnpj']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo ou razão social',
                'required': True,
                'minlength': '3',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'cliente@email.com',
                'required': True,
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000000000 (CPF) ou 00000000000000 (CNPJ)',
                'required': True,
                'pattern': r'[\d\.\-\/]+',
                'title': 'Informe CPF (11 dígitos) ou CNPJ (14 dígitos)',
            }),
        }
        labels = {
            'nome': 'Nome / Razão Social',
            'email': 'E-mail',
            'cpf_cnpj': 'CPF / CNPJ',
        }

    def clean_cpf_cnpj(self):
        value = self.cleaned_data.get('cpf_cnpj', '')
        digits = re.sub(r'\D', '', value)
        if len(digits) not in (11, 14):
            raise forms.ValidationError('CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos.')
        return value


class FaturaForm(forms.ModelForm):
    class Meta:
        model = Fatura
        fields = ['cliente', 'data_emissao', 'valor', 'status', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'data_emissao': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0,00',
                'min': '0.01',
                'step': '0.01',
                'required': True,
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Ex: CFOP 5102, CST 00, NF-e série A...',
            }),
        }
        labels = {
            'cliente': 'Cliente',
            'data_emissao': 'Data de Emissão',
            'valor': 'Valor (R$)',
            'status': 'Status',
            'observacoes': 'Observações (CFOP/CST/Notas)',
        }

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError('O valor deve ser estritamente positivo (maior que zero).')
        return valor

    def clean_data_emissao(self):
        from datetime import date
        data = self.cleaned_data.get('data_emissao')
        if data and data.year < 2000:
            raise forms.ValidationError('Data inválida. Informe uma data a partir do ano 2000.')
        return data