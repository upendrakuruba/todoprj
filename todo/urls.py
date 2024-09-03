from django.urls import path
from .views import *

urlpatterns = [
    path("create_todo/", create_todo, name="create_todo"),
    path("todo_delete/<str:name>/", todo_delete, name="todo_delete"),
    path("update/<str:name>/", update, name="update"),
]
