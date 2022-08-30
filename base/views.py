from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Topic, Room, Message
from .forms import RoomForm


def index(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) |
                                Q(name__icontains=q) |
                                Q(description__icontains=q)
                                )
    topics = Topic.objects.all()
    recent_activity = Message.objects.all().order_by('-created')[:8]
    room_count = rooms.count
    messages_counter = Message.objects.all().count
    title = 'Home page'
    context = {'rooms': rooms,
               'topics': topics,
               'recent_activity': recent_activity,
               'messages_counter': messages_counter,
               'room_count': room_count,
               'title': title
               }
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    title = room.name
    context = {'room': room,
               'room_messages': room_messages,
               'participants': participants,
               'title': title}
    return render(request, 'base/room.html', context)


@login_required(login_url='login-page')
def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    title = 'Create room'
    context = {'form': form, 'title': title}
    return render(request, 'base/create_update_room.html', context)


@login_required(login_url='login-page')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    title = 'Update room'
    context = {'form': form, 'title': title}
    return render(request, 'base/create_update_room.html', context)


@login_required(login_url='login-page')
def delete(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj': room}
    title = 'Shrewder'
    context = {'title': title}
    return render(request, 'base/delete.html', context)


def login_page(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            username = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='login-page')
def logout_user(request):
    logout(request)
    return redirect('login-page')


def register_user(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='login-page')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here!')
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    context = {'obj': message}
    return render(request, 'base/delete.html', context)



