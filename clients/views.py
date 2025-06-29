from django.shortcuts import render, redirect, get_object_or_404
from .models import Client, Note, ClientHistory
from .forms import ClientForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseForbidden
from django.urls import reverse


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    recent_clients = Client.objects.order_by('-created_at')[:5]
    total_clients = Client.objects.count()
    return render(request, 'dashboard.html', {
        'recent_clients': recent_clients,
        'total_clients': total_clients
    })

def client_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    search_query = request.GET.get('q', '')
    clients = Client.objects.all()
    if search_query:
        clients = clients.filter(name__icontains=search_query)
    paginator = Paginator(clients, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'client_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

def client_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    client = get_object_or_404(Client, pk=pk)
    notes = client.notes.order_by('-created_at')
    history = client.history.order_by('-timestamp')
    return render(request, 'client_detail.html', {'client': client, 'notes': notes, 'history': history})

@login_required
def client_add(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            ClientHistory.objects.create(client=client, action='Created', performed_by=request.user)
            messages.success(request, "Client added successfully!")
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    return render(request, 'client_add.html', {'form': form})

@login_required
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            ClientHistory.objects.create(client=client, action='Edited', performed_by=request.user)
            messages.success(request, "Client updated successfully!")
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, 'client_edit.html', {'form': form, 'client': client})

@login_required
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        ClientHistory.objects.create(client=client, action='Deleted', performed_by=request.user)
        client.delete()
        messages.success(request, "Client deleted successfully!")
        return redirect('client_list')
    return render(request, 'client_delete_confirm.html', {'client': client})

@login_required
def client_notes(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Note.objects.create(client=client, author=request.user, content=content)
            ClientHistory.objects.create(client=client, action='Note added', performed_by=request.user, details=content)
            messages.success(request, "Note added!")
            return redirect('client_notes', pk=pk)
    notes = client.notes.order_by('-created_at')
    return render(request, 'client_notes.html', {'client': client, 'notes': notes})

@login_required
def client_history(request, pk):
    client = get_object_or_404(Client, pk=pk)
    history = client.history.order_by('-timestamp')
    return render(request, 'client_history.html', {'client': client, 'history': history})

def monitoring(request):
    if not request.user.is_authenticated:
        return redirect('login')
    total_clients = Client.objects.count()
    total_notes = Note.objects.count()
    total_users = User.objects.count()
    recent_clients = Client.objects.order_by('-created_at')[:5]
    return render(request, 'monitoring.html', {
        'total_clients': total_clients,
        'total_notes': total_notes,
        'total_users': total_users,
        'recent_clients': recent_clients
    })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')