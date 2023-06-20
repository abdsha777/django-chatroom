from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message
from .forms import RoomForm

# rooms=[
#     {'id':1,'name':'learn pyth'},
#     {'id':2,'name':'learn asjasd'},
# ]


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request,"User does not exist")
        
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            message.error(request,"Username or password does not exist")
        
    c={'page':page}
    return render(request,'base/login_register.html',c)

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    c = {"form":form}
    if request.method=="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"An error occurred during registration")
    return render(request,'base/login_register.html',c)
    
def home(request):
    q = request.GET.get('q')  if request.GET.get('q') !=None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))
    print(roomMessages)
    c = {'rooms':rooms,"topics":topics,"room_count":room_count,'room_messages':roomMessages} 
    return render(request,'base/home.html',c)

def room(request,pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method=='POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user )
        return redirect('room',pk=room.id)
    c = {'room':room,'roomMessages':roomMessages,'participants':participants}
    return render(request,"base/room.html",c)

def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    roomMessages = user.message_set.all()
    topics = Topic.objects.all()
    c={'user':user,'rooms':rooms,"room_messages":roomMessages,"topics":topics}
    return render(request,'base/profile.html',c)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
    else:
        c={'form':form,'topics':topics}
        return render(request,'base/room_form.html',c)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('Your are not allowed Here')
    if request.method=="POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    form = RoomForm(instance=room)
    c = {'form':form,'room':room} 
    return render(request,'base/room_form.html',c)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('Your are not allowed Here')
    if request.method=='POST':
        room.delete()
        return redirect('home')
    c={'obj':room}
    return render(request,'base/delete.html',c)

@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse('Your are not allowed Here')
    if request.method=='POST':
        message.delete()
        return redirect('home')
    c={'obj':message}
    return render(request,'base/delete.html',c)
    