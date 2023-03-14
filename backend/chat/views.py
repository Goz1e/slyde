from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.
def dashboard(request):
    template_name = 'chat/dashboard.html'
    context = {
        'title' : f" welcome {request.user.username}",
        'chat_page':'chat_page'
    }
    messages.warning(request,'welcome to dashboard')
    return render(request, template_name, context)

def room(request,room_id):
    room = get_object_or_404(Room,room_id=room_id)
    if room.private:
        if room.admit_user(request.user) != True:
            msg = room.admit_user(request.user)    
            messages.success(request,msg)    
    template_name = 'chat/dashboard.html'
    context = {
        'room':room,
    }
    return render(request, template_name, context)

def room_settings(request,room_id):
    context = {

    }
    template_name = 'chat/dashboard.html'     
    return render(request, template_name, context)
