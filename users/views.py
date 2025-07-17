from django.shortcuts import render

# Create your views here.
def user_main(request):
    return render(request, 'home.html')

def user_signup(request):
    return render(request, 'user_signup.html')

def user_login(request):
    return render(request, 'user_login.html')