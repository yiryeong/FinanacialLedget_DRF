from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from category.models import Category
from expenditure.ExpenditureSerializer import ExpenditureSerializer
from expenditure.models import Expenditure


@permission_classes([IsAuthenticated])
def add_item(request):
    """
    내역 추가
    :param request:
    :return:
    """
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


@permission_classes([IsAuthenticated])
def update_item(request, item_id):
    """
    내역 수정
    :param request:
    :param item_id:
    :return:
    """
    user = request.user
    expenditure = Expenditure.objects.filter(pk=item_id)

    if request.method == 'GET':
        category_list = Category.objects.filter(uid=user)
        serializer = ExpenditureSerializer(expenditure, many=True)
        today = date.today().strftime("%Y-%m-%d")
        context = {"category_list": category_list, "expenditure": serializer.data, "update": True, "today": today}
        return render(request, 'expenditure/update_item.html', context)

    elif request.method == 'POST':
        post_data = request.POST
        serializer = ExpenditureSerializer(post_data)
        serializer.update(expenditure.first(), post_data)
        return redirect('expenditure:list')
