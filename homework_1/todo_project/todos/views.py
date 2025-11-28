from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import TodoForm

def home(request):
    todos = Todo.objects.all().order_by('is_done', 'due_date')
    return render(request, "home.html", {"todos": todos})

def create_todo(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TodoForm()
    return render(request, "todo_form.html", {"form": form})

def edit_todo(request, id):
    todo = get_object_or_404(Todo, id=id)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TodoForm(instance=todo)
    return render(request, "todo_form.html", {"form": form})

def delete_todo(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return redirect("home")

def mark_done(request, id):
    todo = get_object_or_404(Todo, id=id)
    todo.is_done = True
    todo.save()
    return redirect("home")
