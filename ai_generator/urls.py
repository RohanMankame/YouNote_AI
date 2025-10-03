from django.urls import path
from . import views

urlpatterns = [

    path('',views.index, name='index' ),
    path('login',views.user_login, name='login' ),
    path('signup',views.user_signup, name='signup' ),
    path('logout',views.user_logout, name='logout' ),
    path('generate-blog',views.generate_blog, name='generate-blog' ),
    path('note-list',views.note_list, name='note-list' ),
    path('note-details/<int:pk>/',views.note_details, name='note-details' ),

    path('delete-note/<int:pk>/', views.delete_note, name='delete_note'),

    path('edit-note/<int:pk>/', views.edit_note, name='edit_note'),


]