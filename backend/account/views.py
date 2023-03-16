from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout 
from .forms import LoginForm,UserCreationForm
from chat.forms import CreateRoomForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = CreateRoomForm
    return render(request,'account/index.html',{'title':'slyde','form':form})

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, ' you are already logged in')
        return redirect('index')
    form = LoginForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            print('valid form')
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request,user) 
                messages.success(request,'login successfull')
                return redirect('dashboard')
            else:
                messages.success(request,'login failed')
            return redirect('index')
    context= {'title':'slyde', 'form':form} 
    return render(request,'account/login.html',context)


def signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    context= {'form': form,'title':'signup'}
    return render(request, 'account/signup.html',context )

def settings(request):
    context= {'title':'slyde'} 
    return render(request,'account/settings.html',context)


def logout_view(request):
    logout(request)
    messages.info(request,'logout successful')
    return redirect('index')