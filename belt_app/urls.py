from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('success', views.success),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.show_quotes),
    path('delete/<int:id>', views.delete_quote),
    path('user/<int:id>', views.show_user),
    path('add_quote', views.add_quote),
    path('myaccount', views.account),
    path('edit', views.edit),
    path('add_to_favorite/<int:id>', views.add_to_favorite),
    
]


