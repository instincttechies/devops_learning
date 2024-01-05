from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Item
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist

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

class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        return Response(status=status.HTTP_200_OK)

def home(request):
    try:
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
    except Exception as error:
        context = {'welcome_message': f'Technical Error! {error}'}
    return render(request, 'home.html', context)

def signup(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')  # Redirect to login on successful signup
            else:
                return render(request, 'accounts/signup.html', {'form': form})
        else:
            form = UserCreationForm()
    except Exception as error:
        print(f"Error Occured! due to {error}")
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def summary(request):
    items = Item.objects.filter(user=request.user)
    total_price = sum(item.price for item in items)

    return render(request, 'summary.html', {'total_price': total_price})

