
'''
# Create your views here.
from django.shortcuts import render, redirect
from .models import Task

def index(request):
    tasks = Task.objects.all()
    return render(request, 'todo/index.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        Task.objects.create(title=title)
    return redirect('index')

def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('index')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')
'''
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from datetime import datetime,date

def index(request):
    show_overdue = request.GET.get('show') == 'overdue'
    today = date.today()

    if show_overdue:
        tasks = Task.objects.filter(due_date__lt=today, completed=False).order_by('due_date')
    else:
        tasks = Task.objects.filter(completed=False).order_by('due_date')  # 👈 exclude completed

    return render(request, 'todo/index.html', {
        'tasks': tasks,
        'today': today,
        'show_overdue': show_overdue
    })


def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        due_date = request.POST.get('due_date')  # safer with .get()
        if due_date:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        else:
            due_date = None
        Task.objects.create(title=title, due_date=due_date)
    return redirect('index')
def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('index')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('index')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        task.title = request.POST['title']
        due_date = request.POST.get('due_date')
        task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None
        task.save()
        return redirect('index')

    return render(request, 'todo/edit.html', {
        'task': task
    })
def completed_tasks(request):
    tasks = Task.objects.filter(completed=True).order_by('-due_date')
    return render(request, 'todo/completed.html', {'tasks': tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed  # ✅ toggles completed/incomplete
    task.save()
    return redirect(request.META.get('HTTP_REFERER', 'index'))  # 👈 return to previous page

