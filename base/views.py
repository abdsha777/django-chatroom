from django.shortcuts import render,redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Room,Topic
from .forms import RoomForm

# rooms=[
#     {'id':1,'name':'learn pyth'},
#     {'id':2,'name':'learn asjasd'},
# ]


# Create your views here.

def loginPage(request):
    if request.method=="POST":
        username=request.POST.get('username')
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
        
    c={}
    return render(request,'base/login_register.html',c)

def home(request):
    q = request.GET.get('q')  if request.GET.get('q') !=None else ''
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    
    c = {'rooms':rooms,"topics":topics,"room_count":room_count} 
    return render(request,'base/home.html',c)

def room(request,pk):
    room = Room.objects.get(id=pk)
    # for i in rooms:
    #     if i['id']== int(pk):
    #         room=i    
    c = {'room':room}
    return render(request,"base/room.html",c)

def createRoom(request):
    if request.method=="POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm()
        c={'form':form}
        return render(request,'base/room_form.html',c)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method=="POST":
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    form = RoomForm(instance=room)
    c = {'form':form}
    return render(request,'base/room_form.html',c)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    c={'obj':room}
    return render(request,'base/delete.html',c)

