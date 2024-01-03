from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Item
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated:
        username = request.user.username
        items = Item.objects.filter(user=request.user)

        if request.method == 'POST':
            for item in items:
                item_name = request.POST.get(f'item{item.id}')
                item_price = request.POST.get(f'price{item.id}')

                item.name = item_name
                item.price = item_price
                item.save()

            new_item_name = request.POST.get('new_item_name')
            new_item_price = request.POST.get('new_item_price')
            if new_item_name and new_item_price:
                new_item = Item.objects.create(user=request.user, name=new_item_name, price=new_item_price)
            return redirect('home')
        else:
            context = {'welcome_message': f'Welcome {username}', 'items':items}
    else:
        context = {'welcome_message': 'Welcome to the Home Page'}

    return render(request, 'home.html', context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login on successful signup
        else:
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

from .models import Item

@login_required
def summary(request):
    items = Item.objects.filter(user=request.user)
    total_price = sum(item.price for item in items)

    return render(request, 'summary.html', {'total_price': total_price})

def dashboard(request):
    items = Item.objects.filter(user=request.user)

    if request.method == 'POST':
        for item in items:
            item_name = request.POST.get(f'item{item.id}')
            item_price = request.POST.get(f'price{item.id}')

            item.name = item_name
            item.price = item_price
            item.save()

        new_item_name = request.POST.get('new_item_name')
        new_item_price = request.POST.get('new_item_price')
        if new_item_name and new_item_price:
            new_item = Item.objects.create(user=request.user, name=new_item_name, price=new_item_price)

        return redirect('dashboard')

    return render(request, 'dashboard.html', {'items': items})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('home')