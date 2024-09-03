from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

@login_required(login_url='login')
def create_todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo=Todo(user=request.user,todo_name=task)
        new_todo.save()
        return redirect('home')
    return render(request,'todo.html')


def todo_delete(request,name):
    get_todo=get_object_or_404(Todo,user=request.user,todo_name=name)
    context = {
        'get_todo':get_todo
    }
    if request.method == 'POST':
        get_todo.delete()
        return HttpResponseRedirect(reverse('home'))
    return render(request,'delete_alerts.html',context)



def update(request,name):
    get_todo = Todo.objects.get(user=request.user,todo_name=name)
    get_todo.status = True
    get_todo.save()
    return redirect('home')


# todo=get_object_or_404(Todo,pk=id,user=request.user)
#     if request.method == 'POST':
#         form = TodoForm(request.POST,instance=todo)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('todo',kwargs={'id':todo.pk}))
#     else:
#         form = TodoForm(instance=todo)



