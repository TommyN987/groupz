from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Group, Topic, Message
from .forms import GroupForm


def login_page(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''

    groups = Group.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    group_count = groups.count()

    context = {'groups': groups, 'group_count': group_count, 'topics': topics}

    return render(request, 'base/home.html', context)


def group(request, pk):
    group = Group.objects.get(id=pk)
    room_messages = group.message_set.all().order_by('-created')  # type: ignore
    participants = group.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            group=group,
            body=request.POST.get('body')
        )
        group.participants.add(request.user)
        return redirect('group', pk=group.id)  # type: ignore

    context = {'group': group, 'room_messages': room_messages, 'participants': participants}

    return render(request, 'base/group.html', context)


@login_required(login_url='/login')
def create_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/group_form.html', context)


@login_required(login_url='/login')
def update_group(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)

    if request.user != group.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/group_form.html', context)


@login_required(login_url='/login')
def delete_group(request, pk):
    group = Group.objects.get(id=pk)

    if request.user != group.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        group.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': group})


@login_required(login_url='/login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})
