from django.urls import path
# from . import views
from .views import base_views, add_item_views


app_name = 'expenditure'

urlpatterns = [
    path('', base_views.expenditure, name='list'),
    path('add_item/', add_item_views.add_item, name='add_item'),
    # path('<int:category_id>', views.expenditure_detail, name='detail'),
]
