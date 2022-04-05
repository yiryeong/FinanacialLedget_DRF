from django.urls import path
from .views import base_views, item_views


app_name = 'expenditure'

urlpatterns = [
    path('', base_views.expenditure, name='list'),
    path('add_item/', item_views.add_item, name='add_item'),
    path('update_item/<item_id>', item_views.update_item, name='update_item'),
    path('delete_item/<item_id>', item_views.delete_item, name='delete_item'),
]
