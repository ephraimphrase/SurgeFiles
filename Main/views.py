from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.utils import timezone
import uuid
from django.db.models import Q
from Main.models import Files, Folder


# ─── Landing ────────────────────────────────────────────────────────────────

def landing(request):
    title = 'Landing Page'
    context = {'title': title}
    return render(request, 'index.html', context)


# ─── Dashboard ──────────────────────────────────────────────────────────────

@login_required(login_url='login')
def dashboard(request):
    search_query = request.GET.get('search_query', '')
    sort_by = request.GET.get('sort', '-date')
    folder_id = request.GET.get('folder', '')

    files = Files.objects.filter(owner=request.user, is_trashed=False)

    # Filter by folder
    if folder_id == 'none':
        # Show only root-level files (no folder)
        files = files.filter(folder__isnull=True)
    elif folder_id:
        files = files.filter(folder_id=folder_id)

    # Search (OR logic across title and description)
    if search_query:
        files = files.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Sorting
    sort_options = {
        '-date': '-date',
        'date': 'date',
        'title': 'title',
        '-title': '-title',
        '-size': '-size',
        'size': 'size',
    }
    order = sort_options.get(sort_by, '-date')
    files = files.order_by(order)

    # Pagination (12 per page)
    paginator = Paginator(files, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # User's folders for the sidebar
    folders = Folder.objects.filter(owner=request.user)

    # Count files in trash for badge
    trash_count = Files.objects.filter(owner=request.user, is_trashed=True).count()

    context = {
        'title': 'Dashboard',
        'files': page_obj,
        'folders': folders,
        'search_query': search_query,
        'current_sort': sort_by,
        'current_folder': folder_id,
        'trash_count': trash_count,
    }
    return render(request, 'dashboard.html', context)


# ─── Auth ───────────────────────────────────────────────────────────────────

def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'register.html', {'title': 'Register'})

    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip()
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    if not username or not password:
        messages.error(request, 'Username and password are required.')
        return render(request, 'register.html', {'title': 'Register'})

    try:
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=password,
        )
    except IntegrityError:
        messages.error(request, 'That username is already taken. Please choose another.')
        return render(request, 'register.html', {'title': 'Register'})

    login(request, user)
    messages.success(request, 'Signed up successfully!')
    return redirect('dashboard')


def loginUser(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'login.html', {'title': 'Log In'})

    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')

    if not User.objects.filter(username=username).exists():
        messages.error(request, 'No account found with that username.')
        return render(request, 'login.html', {'title': 'Log In'})

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, 'Logged in successfully!')
        return redirect('dashboard')

    messages.error(request, 'Incorrect password. Please try again.')
    return render(request, 'login.html', {'title': 'Log In'})


@require_POST
def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── File Operations ────────────────────────────────────────────────────────

@login_required(login_url='login')
def addFile(request):
    if request.method == 'GET':
        folders = Folder.objects.filter(owner=request.user)
        context = {'title': 'Upload File', 'folders': folders}
        return render(request, 'addFile.html', context)

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()
    folder_id = request.POST.get('folder', '').strip()
    file = request.FILES.get('file')

    if not file:
        messages.error(request, 'Please select a file to upload.')
        folders = Folder.objects.filter(owner=request.user)
        return render(request, 'addFile.html', {'title': 'Upload File', 'folders': folders})

    if not title:
        messages.error(request, 'Please give your file a title.')
        folders = Folder.objects.filter(owner=request.user)
        return render(request, 'addFile.html', {'title': 'Upload File', 'folders': folders})

    # Resolve folder
    folder = None
    if folder_id:
        folder = Folder.objects.filter(id=folder_id, owner=request.user).first()

    Files.objects.create(
        id=str(uuid.uuid4())[:8],
        title=title,
        description=description,
        file=file,
        owner=request.user,
        folder=folder,
        size=file.size,
    )
    messages.success(request, f'"{title}" uploaded successfully!')
    return redirect('dashboard')


@login_required(login_url='login')
def editFile(request, id):
    file = get_object_or_404(Files, id=id)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not have permission to edit this file.')

    if request.method == 'GET':
        folders = Folder.objects.filter(owner=request.user)
        context = {'title': 'Edit File', 'file': file, 'folders': folders}
        return render(request, 'editFile.html', context)

    file.title = request.POST.get('title', file.title).strip()
    file.description = request.POST.get('description', file.description).strip()
    folder_id = request.POST.get('folder', '').strip()

    if folder_id:
        file.folder = Folder.objects.filter(id=folder_id, owner=request.user).first()
    else:
        file.folder = None

    file.save()
    messages.success(request, f'"{file.title}" updated.')
    return redirect('dashboard')


@login_required(login_url='login')
def downloadFile(request, id):
    file = get_object_or_404(Files, id=id)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not have permission to access this file.')
    context = {'title': 'Download File', 'file': file}
    return render(request, 'downloadFile.html', context)


@login_required(login_url='login')
def trashFile(request, id):
    """Soft-delete: move file to trash."""
    file = get_object_or_404(Files, id=id)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not have permission to delete this file.')
    file.is_trashed = True
    file.trashed_at = timezone.now()
    file.save()
    messages.success(request, f'"{file.title}" moved to trash.')
    return redirect('dashboard')


@login_required(login_url='login')
def trashView(request):
    """Show all trashed files."""
    trashed = Files.objects.filter(owner=request.user, is_trashed=True).order_by('-trashed_at')
    context = {'title': 'Trash', 'files': trashed}
    return render(request, 'trash.html', context)


@login_required(login_url='login')
def restoreFile(request, id):
    """Restore a file from trash."""
    file = get_object_or_404(Files, id=id, is_trashed=True)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not have permission to restore this file.')
    file.is_trashed = False
    file.trashed_at = None
    file.save()
    messages.success(request, f'"{file.title}" has been restored.')
    return redirect('trash')


@login_required(login_url='login')
def permanentDelete(request, id):
    """Permanently delete a file from trash."""
    file = get_object_or_404(Files, id=id, is_trashed=True)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not have permission to delete this file.')
    title = file.title
    file.delete()
    messages.success(request, f'"{title}" permanently deleted.')
    return redirect('trash')


# ─── Sharing ────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def shareFile(request, id):
    """Generate or revoke a public share link."""
    file = get_object_or_404(Files, id=id)
    if file.owner != request.user:
        return HttpResponseForbidden('You do not have permission to share this file.')

    if file.share_id:
        # Revoke existing share
        file.share_id = None
        file.save()
        messages.info(request, f'Share link for "{file.title}" has been revoked.')
    else:
        # Generate a new share link
        file.share_id = uuid.uuid4().hex[:16]
        file.save()
        messages.success(request, f'Share link created for "{file.title}"!')

    return redirect('dashboard')


def sharedFile(request, share_id):
    """Public download page — no login required."""
    file = get_object_or_404(Files, share_id=share_id, is_trashed=False)
    context = {'title': f'{file.title} — Shared File', 'file': file}
    return render(request, 'sharedFile.html', context)


# ─── Folders ────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def createFolder(request):
    if request.method == 'GET':
        return render(request, 'createFolder.html', {'title': 'New Folder'})

    name = request.POST.get('name', '').strip()
    if not name:
        messages.error(request, 'Folder name is required.')
        return render(request, 'createFolder.html', {'title': 'New Folder'})

    # Check for duplicate folder name
    if Folder.objects.filter(owner=request.user, name=name).exists():
        messages.error(request, f'You already have a folder named "{name}".')
        return render(request, 'createFolder.html', {'title': 'New Folder'})

    Folder.objects.create(
        id=str(uuid.uuid4())[:8],
        name=name,
        owner=request.user,
    )
    messages.success(request, f'Folder "{name}" created.')
    return redirect('dashboard')


@login_required(login_url='login')
def deleteFolder(request, id):
    folder = get_object_or_404(Folder, id=id)
    if folder.owner != request.user:
        return HttpResponseForbidden('You do not have permission to delete this folder.')

    # Move files out of the folder before deleting it
    folder.files.update(folder=None)
    name = folder.name
    folder.delete()
    messages.success(request, f'Folder "{name}" deleted. Files moved to root.')
    return redirect('dashboard')


# ─── Profile ────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def profile(request):
    if request.method == 'GET':
        context = {'title': 'Profile'}
        return render(request, 'profile.html', context)

    user = request.user
    user.first_name = request.POST.get('first_name', user.first_name).strip()
    user.last_name = request.POST.get('last_name', user.last_name).strip()
    user.email = request.POST.get('email', user.email).strip()

    new_password = request.POST.get('new_password', '').strip()
    if new_password:
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated successfully.')
    else:
        user.save()

    messages.success(request, 'Profile updated.')
    return redirect('profile')