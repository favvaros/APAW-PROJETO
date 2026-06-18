# ARQUIVO: faturamento/models.py
# Substitua TODO o conteúdo do arquivo faturamento/models.py por este:

from django.db import models
from django.core.validators import EmailValidator, MinValueValidator
import re
from django.core.exceptions import ValidationError


def validar_cpf_cnpj(value):
    """Valida CPF (11 dígitos) ou CNPJ (14 dígitos) — aceita apenas números."""
    digits = re.sub(r'\D', '', value)
    if len(digits) not in (11, 14):
        raise ValidationError(
            'CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos. Informe apenas números.'
        )


class Cliente(models.Model):
    nome = models.CharField(max_length=200, verbose_name='Nome Completo / Razão Social')
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator(message='Informe um endereço de e-mail válido.')],
        verbose_name='E-mail'
    )
    cpf_cnpj = models.CharField(
        max_length=18,
        verbose_name='CPF / CNPJ',
        validators=[validar_cpf_cnpj],
        help_text='Informe apenas números (CPF: 11 dígitos, CNPJ: 14 dígitos)'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def cpf_cnpj_formatado(self):
        digits = re.sub(r'\D', '', self.cpf_cnpj)
        if len(digits) == 11:
            return f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}'
        elif len(digits) == 14:
            return f'{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}'
        return self.cpf_cnpj


class Fatura(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('paga', 'Paga'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='faturas',
        verbose_name='Cliente'
    )
    data_emissao = models.DateField(verbose_name='Data de Emissão')
    valor = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='O valor da fatura deve ser positivo.')],
        verbose_name='Valor (R$)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
        verbose_name='Status'
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações',
        help_text='Notas fiscais, CFOP/CST aplicável, informações adicionais.'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-data_emissao']

    def __str__(self):
        return f'Fatura #{self.pk} — {self.cliente.nome} — R$ {self.valor}'

    def status_badge(self):
        badges = {
            'pendente': 'warning',
            'paga': 'success',
            'cancelada': 'danger',
        }
        return badges.get(self.status, 'secondary')