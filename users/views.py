from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login

# Create your views here.
def user_main(request):
    return render(request, 'home.html')

def user_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:user_login')  # 회원가입 후 이동할 페이지
    else:
        form = CustomUserCreationForm()
    return render(request, 'user_signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('users:user_main')  # 로그인 후 이동할 페이지
    else:
        form = AuthenticationForm()
    return render(request, 'user_login.html', {'form': form})