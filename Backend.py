# Import necessary modules
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import SignIn

# View for sign in form
def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            SignIn.objects.create(user=user, ip_address=request.META.get('REMOTE_ADDR'))
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            else:
                # Set session expiration to two weeks if "remember me" is checked
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

# View for creating a new user account
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# View for forgot password form
def forgot_password_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})

# View for setting a new password
def reset_password_view(request, uidb64, token):
    if request.method == 'POST':
        form = SetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_complete')
    else:
        form = SetPasswordForm(user=request.user)
    return render(request, 'reset_password.html', {'form': form})

# View for sign out
@login_required
def signout_view(request):
    logout(request)
    return redirect('home')

# View for sign up form
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
# login form done #



# Database#
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class SignIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    remember_me = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

class SignUp(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class ForgotPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


#Django Rest Framework API for the sign in, sign out, create account, and forgot password features #
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from .models import SignIn

# API endpoint for sign in
@api_view(['POST'])
def signin_view(request):
    form = AuthenticationForm(data=request.data)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        SignIn.objects.create(user=user, ip_address=request.META.get('REMOTE_ADDR'), remember_me=request.data.get('remember_me', False))
        return Response({'message': 'Successfully signed in.'}, status=status.HTTP_200_OK)
    else:
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for creating a new account
@api_view(['POST'])
def create_account_view(request):
    form = UserCreationForm(request.data)
    if form.is_valid():
        form.save()
        return Response({'message': 'Successfully created account.'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for forgot password
@api_view(['POST'])
def forgot_password_view(request):
    form = PasswordResetForm(request.data)
    if form.is_valid():
        form.save(request=request)
        return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
    else:
        return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for setting a new password
@api_view(['POST'])
def reset_password_view(request):
    uidb64 = request.data.get('uidb64')
    token = request.data.get('token')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        form = SetPasswordForm(user=user, data=request.data)
        if form.is_valid():
            form.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
    return Response({'errors': 'Invalid reset link.'}, status=status.HTTP_400_BAD_REQUEST)

# API endpoint for signing out
@api_view(['POST'])
def signout_view(request):
    logout(request)
    return Response({'message': 'Successfully signed out.'}, status=status.HTTP_200_OK)
