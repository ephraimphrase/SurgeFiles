from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import uuid
from django.db.models import Q
from Main.models import Files

# Create your views here.
def landing(request):
    title = 'Landing Page'
    context = {'title':title}
    return render(request, 'index.html', context)

@login_required(login_url='login')
def dashboard(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    files = Files.objects.filter(Q(title__icontains=search_query), Q(description__icontains=search_query),owner=request.user)
    title = 'Dashboard'
    context = {'title':title, 'files':files}
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == "GET":
        title = 'Register'
        context = {'title':title}
        return render(request, 'register.html', context)
    
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
        user.save()

        login(request, user)
        messages.success(request, 'Signed up successfully')
        return redirect('dashboard')

def loginUser(request):
    if request.method == "GET":
        return render(request, 'login.html')

    else:
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Logged In Succesfully')
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect username or password')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.info(request, 'User logged out')
    return redirect('login')

@login_required(login_url='login')
def addFile(request):
    if request.method == "GET":
        title = 'Add File'
        context = {'title':title}
        return render(request, 'addFile.html', context)

    else:
        title= request.POST['title']
        description = request.POST['description']
        file = request.FILES['file']

        files = Files.objects.create(id=str(uuid.uuid4())[:5], title=title, description=description, file=file, owner=request.user)
        files.save()
        return redirect('dashboard')

@login_required(login_url='login')
def downloadFile(request, id):
    title = 'Download File'
    file = get_object_or_404(Files, id=id)
    context = {'title':title, 'file':file}
    return render(request, 'downloadFile.html', context)

@login_required(login_url='login')
def deleteFile(request, id):
    file = Files.objects.get(id=id)
    # if request.method == "POST":
    if file.owner == request.user:
        file.delete()
        return redirect('dashboard')