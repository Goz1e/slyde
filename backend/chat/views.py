from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from .forms import RoomForm, CreateRoomForm
from guardian.utils import get_anonymous_user
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm
# from guardian.shortcuts import assign_perm

# def perm_check(room,user):
#     return bool(
#         user.has_perm('chat.super_admin',room)
#     )
# super_admins = Group.objects.get(name='super admin')

# Create your views here.
def create_room(request):
    if request.POST:
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            if request.user.is_authenticated:
                room.owner = request.user
                # room.owner.groups.add(super_admins)
            else:
                room.owner = get_anonymous_user()
                # room.allow_anon = True
                # room.owner.groups.add(super_admins)
            room.save()
            # assign_perm('super_admin',room.owner,room)
            msg = f'{room.name} created with ID: {room.room_id}'
            return redirect('room',room.room_id)
        msg = 'room creation failed'
        messages.info(request,msg)
        return redirect('index')

def dashboard(request):
    rooms = Room.objects.all_rooms(request.user)
    form = CreateRoomForm(request.POST)
    template_name = 'chat/dashboard.html'
    context = {
        'title' : f" welcome {request.user.username}",
        'chat_page':'chat_page',
        'form':form
    }
    if rooms.exists():
        context['rooms']=rooms
    return render(request, template_name, context)

def get_room(request):
    room_id = request.GET.get('q')
    try:
        room = get_object_or_404(Room,room_id=room_id)
        return redirect('room',room.room_id)
    except:
        messages.info(request,f'room with id: {room_id} does not exist')
        if request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('index')


def room(request,room_id):
    room = get_object_or_404(Room,room_id=room_id)
    access = room.admit_user(request.user)
    if access !=True:
        messages.info(request,access)
        if request.user.is_authenticated:
            return redirect('dashboard')
        return redirect('index')
    context = {
        'room':room, 'title':room.name, 'chat_page':'chat_page'
    }
    return render(request,'chat/room.html',context)

    
# @user_passes_test(email_check)
def room_settings(request,room_id):
    room = get_object_or_404(Room,room_id=room_id)
    form = CreateRoomForm(request.POST or None, instance=room)
    if request.user.is_authenticated:
        form = RoomForm(request.POST or None, instance=room)
    if request.POST:
        print('request is POST')
        if form.is_valid():
            form.save()
            return redirect('room',room.room_id)
    context = {
        'room':room, 'members':room.members.all(), 'admins':room.room_admin.all(),
        'room_requests':room.requests.all(), 'form':form, 'title': f'{room.name} settings'
    }
    if room.has_access(request.user):
        context['admin_access'] = 'admin_access'
    if room.has_prem_access(request.user):
        context['prem_access'] = 'prem_access'
    template_name = 'chat/room_settings.html'     
    return render(request, template_name, context)


def admin_actions(request,room_id,username,action):
    room = get_object_or_404(Room,room_id=room_id)
    user = get_object_or_404(User,username=username)
    command = {
        'accept':room.approve_requests,
        'decline':room.decline_requests,
        'remove':room.remove_member,
        'make_admin':room.make_admin,
        'revoke_admin':room.revoke_admin,
        'accept_all':room.approve_all_requests,
        'decline_all':room.decline_all_requests,
    }

    if command[action](request.user,user):
        messages.success(request, f'{action} successful!')
        return redirect('room_settings',room_id)
    messages.warning(request, f'{action} failed')    
    return redirect('room_settings',room_id)