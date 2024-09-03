from django.shortcuts import render
from todo.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.


def get_showing_todos(request,all_todo):

    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'completed':
            return all_todo.filter(status=True)
        if request.GET.get('filter') == 'incompleted':
            return all_todo.filter(status=False)
        
    return all_todo


@login_required(login_url='login')
def home(request):
    all_todo=Todo.objects.filter(user=request.user)
    completed_count = all_todo.filter(status=True).count()
    incompleted_count = all_todo.filter(status=False).count()
    all_count = all_todo.count()
    context = {
        'all_todo':get_showing_todos(request,all_todo),
        'completed_count':completed_count,
        'incompleted_count':incompleted_count,
        'all_count':all_count
    }
    return render(request,'todo.html',context)