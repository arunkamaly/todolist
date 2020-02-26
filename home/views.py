from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from home.models import TodoList, Todo
from home.forms import TodoForm, TodoListForm


def index(request):
    return render(request, 'home/index.html', {'form': TodoForm()})


def todolist(request, todolist_id):
    todolist = get_object_or_404(TodoList, pk=todolist_id)
    if request.method == 'POST':
        redirect('home:add_todo', todolist_id=todolist_id)

    return render(
        request, 'home/todolist.html',
        {'todolist': todolist, 'form': TodoForm()}
    )


def add_todo(request, todolist_id):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todo = Todo(
                description=request.POST['description'],
                todolist_id=todolist_id,
                creator=user
            )
            todo.save()
            return redirect('home:todolist', todolist_id=todolist_id)
        else: 
            return render(request, 'home/todolist.html', {'form': form})

    return redirect('home:index')


@login_required
def overview(request):
    if request.method == 'POST':
        return redirect('home:add_todolist')
    print("*********")
    return render(request, 'home/overview.html', {'form': TodoListForm()})


def new_todolist(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            # create default todolist
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(creator=user)
            todolist.save()
            todo = Todo(
                description=request.POST['description'],
                todolist_id=todolist.id,
                creator=user
            )
            todo.save()
            return redirect('home:todolist', todolist_id=todolist.id)
        else:
            return render(request, 'home/index.html', {'form': form})

    return redirect('home:index')


def add_todolist(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            user = request.user if request.user.is_authenticated else None
            todolist = TodoList(title=request.POST['title'], creator=user)
            todolist.save()
            return redirect('home:todolist', todolist_id=todolist.id)
        else:
            return render(request, 'home/overview.html', {'form': form})

    return redirect('home:index')
