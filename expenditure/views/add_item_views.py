from datetime import date
from django.shortcuts import render, redirect
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from category.models import Category
from expenditure.ExpenditureSerializer import ExpenditureSerializer


@permission_classes([IsAuthenticated])
def add_item(request):
    user = request.user

    if request.method == 'GET':
        category_list = Category.objects.filter(uid=user)
        return render(request, 'expenditure/add_item.html', {"category_list": category_list})

    elif request.method == 'POST':
        post_data = request.POST

        expenditure_info = {
            'pay_date': post_data['pay_date'],
            'uid': user.id,
            'price': post_data['price'],
            'product': post_data['product'],
            'cid': post_data['category'],
        }

        if post_data['place'] != "":
            expenditure_info['place'] = post_data['place']

        if post_data['memo'] != "":
            expenditure_info['memo'] = post_data['memo']

        serializer = ExpenditureSerializer(data=expenditure_info)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('expenditure:list')
