from django.urls import path
from . import views


app_name = 'category'


urlpatterns = [
    path('', views.category, name='list'),
    path('modify/<int:category_id>', views.category_modify, name='modify'),
    path('delete/<int:category_id>', views.category_delete, name='delete'),
]
