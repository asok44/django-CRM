from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    #fetch records from database
    records = Record.objects.all()


    #check to see if user is logged in
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        #authenticate user
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in!'))
            return redirect('home')
        else:
            messages.success(request, ('Error logging in - please try again...'))
            return redirect('home')
    else:
        return render(request, 'home.html', {'records' : records})
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been logged out!'))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate user and log them in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, ('You have been registered! Welcome!!'))
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form' : form})

    return render(request, 'register.html', {'form' : form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        #get record from database by id
        customer_record = Record.objects.get(id = pk)
        return render(request, 'record.html', {'customer_record' : customer_record})
    else:
        messages.success(request, ('Please log in to view customer records...'))
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id = pk)
        customer_record.delete()
        messages.success(request, ('Record has been deleted...'))
        return redirect('home')
    else:
        messages.success(request, ('Please log in to delete customer records...'))
        return redirect('home')
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, ('Record has been added...'))
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.success(request, ('Please log in to add customer records...'))
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance = record)
        if form.is_valid():
            form.save()
            messages.success(request, ('Record has been updated...'))
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, ('Please log in to update customer records...'))
        return redirect('home')