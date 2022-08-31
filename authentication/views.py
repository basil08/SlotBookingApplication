from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
# from authentication.models import User
from authentication.models import User
from .forms import SignupForm

def login(request):
  if request.method == 'POST':
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)

    if username is None or password is None:
      messages.error(request, "Please provide username and password!")
      return render(request, 'authentication/login.html')

    user = authenticate(username=username, password=password)

    if user is not None:
      auth_login(request, user)
      return redirect('sport:dashboard')
    else:
      error_message = "Username / Password combination incorrect. Try again!"
      messages.error(request, error_message)
      return render(request, 'authentication/login.html')
  else:
    return render(request, 'authentication/login.html')

def signup(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      first_name = form.cleaned_data.get('first_name', None)
      last_name = form.cleaned_data.get('last_name', None)
      password = form.cleaned_data.get('password', None)
      password_again = form.cleaned_data.get('password_again', None)
      username = form.cleaned_data.get('username', None)
      email  = form.cleaned_data.get('email', None)
      type = form.cleaned_data.get('account_type', None)

      if password != password_again:
        messages.error(request, "Password doesn't match! Try Again!")
        return render(request, 'authentication/signup.html')

      # unique username
      usernames = User.objects.filter(username=username)
      if len(usernames) != 0:
        messages.error(request, "This username is taken! Please try again!")
        return render(request, 'authentication/signup.html')

      if type == 'USER':
        level = 300
      elif type == 'STAFF':
        level = 200
      elif type == 'ADMIN':
        level = 100

      user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        level=level,
      )

      user.set_password(password)
      user.save()

      messages.success(request, 'Account created successfully!')
      return render(request, 'authentication/signup.html')
    else:
      messages.error(request, "Bahut saare errors hai. Pehle theek karo phir try karna")
      return render(request, 'authentication/signup.html')
  else:
    form = SignupForm()
  return render(request, 'authentication/signup.html', { 'form': form })


def logoutUser(request):
  logout(request)
  return redirect('authentication:login')
