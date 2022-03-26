from django.urls import path
from . import views


app_name = 'expenditure'

urlpatterns = [
    path('', views.expenditure, name='list'),
    # path('<int:category_id>', views.expenditure_detail, name='detail'),
]
