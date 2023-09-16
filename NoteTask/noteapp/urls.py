from django.urls import path
from . import views

urlpatterns = [
    path('create-note', views.create_note, name='create'),
    path('get-note', views.list_notes, name='get'),
    path('get-note/<int:id>', views.retrieve_note, name='retrieve'),
    path('update-note/<int:id>', views.update_note, name='update'),
    path('patch-note/<int:id>', views.patch_note, name='patch'),
    path('delete-note/<int:id>', views.delete_note, name='delete'),
    path('register', views.register, name='register'),
]
