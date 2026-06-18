# ARQUIVO: faturamento/views.py
# Substitua TODO o conteúdo do arquivo faturamento/views.py por este:

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum, Count
from decimal import Decimal

from .models import Cliente, Fatura
from .forms import RegistroUsuarioForm, ClienteForm, FaturaForm


# ─────────────────────────── AUTENTICAÇÃO ───────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos. Tente novamente.')
    else:
        form = AuthenticationForm()

    return render(request, 'faturamento/login.html', {'form': form})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Corrija os erros abaixo para criar sua conta.')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'faturamento/registro.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu do sistema com segurança.')
    return redirect('login')


# ─────────────────────────── DASHBOARD ───────────────────────────

@login_required
def dashboard_view(request):
    total_clientes = Cliente.objects.count()
    total_faturas = Fatura.objects.count()

    faturas_pendentes = Fatura.objects.filter(status='pendente')
    soma_pendentes = faturas_pendentes.aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    qtd_pendentes = faturas_pendentes.count()

    soma_pagas = Fatura.objects.filter(status='paga').aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
    qtd_pagas = Fatura.objects.filter(status='paga').count()

    ultimas_faturas = Fatura.objects.select_related('cliente').order_by('-criado_em')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_faturas': total_faturas,
        'soma_pendentes': soma_pendentes,
        'qtd_pendentes': qtd_pendentes,
        'soma_pagas': soma_pagas,
        'qtd_pagas': qtd_pagas,
        'ultimas_faturas': ultimas_faturas,
    }
    return render(request, 'faturamento/dashboard.html', context)


# ─────────────────────────── CLIENTES ───────────────────────────

@login_required
def cliente_lista(request):
    clientes = Cliente.objects.annotate(total_faturas=Count('faturas')).order_by('nome')
    return render(request, 'faturamento/cliente_lista.html', {'clientes': clientes})


@login_required
def cliente_criar(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nome}" cadastrado com sucesso!')
            return redirect('cliente_lista')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = ClienteForm()

    return render(request, 'faturamento/cliente_form.html', {'form': form, 'titulo': 'Novo Cliente', 'acao': 'Cadastrar'})


@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cliente "{cliente.nome}" atualizado com sucesso!')
            return redirect('cliente_lista')
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'faturamento/cliente_form.html', {
        'form': form,
        'titulo': f'Editar: {cliente.nome}',
        'acao': 'Salvar Alterações',
        'cliente': cliente,
    })


@login_required
def cliente_excluir(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        nome = cliente.nome
        try:
            cliente.delete()
            messages.success(request, f'Cliente "{nome}" excluído com sucesso!')
        except Exception:
            messages.error(request, f'Não é possível excluir "{nome}" pois há faturas vinculadas.')
        return redirect('cliente_lista')

    return render(request, 'faturamento/confirmar_exclusao.html', {
        'objeto': cliente,
        'tipo': 'Cliente',
        'cancelar_url': 'cliente_lista',
    })


# ─────────────────────────── FATURAS ───────────────────────────

@login_required
def fatura_lista(request):
    status_filtro = request.GET.get('status', '')
    faturas = Fatura.objects.select_related('cliente').order_by('-data_emissao')
    if status_filtro:
        faturas = faturas.filter(status=status_filtro)

    context = {
        'faturas': faturas,
        'status_filtro': status_filtro,
        'status_choices': Fatura.STATUS_CHOICES,
    }
    return render(request, 'faturamento/fatura_lista.html', context)


@login_required
def fatura_detalhe(request, pk):
    fatura = get_object_or_404(Fatura.objects.select_related('cliente'), pk=pk)
    return render(request, 'faturamento/fatura_detalhe.html', {'fatura': fatura})


@login_required
def fatura_criar(request):
    if request.method == 'POST':
        form = FaturaForm(request.POST)
        if form.is_valid():
            fatura = form.save()
            messages.success(request, f'Fatura #{fatura.pk} criada com sucesso!')
            return redirect('fatura_detalhe', pk=fatura.pk)
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FaturaForm()

    return render(request, 'faturamento/fatura_form.html', {'form': form, 'titulo': 'Nova Fatura', 'acao': 'Emitir Fatura'})


@login_required
def fatura_editar(request, pk):
    fatura = get_object_or_404(Fatura, pk=pk)

    if request.method == 'POST':
        form = FaturaForm(request.POST, instance=fatura)
        if form.is_valid():
            form.save()
            messages.success(request, f'Fatura #{fatura.pk} atualizada com sucesso!')
            return redirect('fatura_detalhe', pk=fatura.pk)
        else:
            messages.error(request, 'Corrija os erros no formulário.')
    else:
        form = FaturaForm(instance=fatura)

    return render(request, 'faturamento/fatura_form.html', {
        'form': form,
        'titulo': f'Editar Fatura #{fatura.pk}',
        'acao': 'Salvar Alterações',
        'fatura': fatura,
    })


@login_required
def fatura_excluir(request, pk):
    fatura = get_object_or_404(Fatura, pk=pk)

    if request.method == 'POST':
        fatura_id = fatura.pk
        fatura.delete()
        messages.success(request, f'Fatura #{fatura_id} excluída com sucesso!')
        return redirect('fatura_lista')

    return render(request, 'faturamento/confirmar_exclusao.html', {
        'objeto': fatura,
        'tipo': 'Fatura',
        'cancelar_url': 'fatura_lista',
    })