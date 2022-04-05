from datetime import date
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from requests import Response
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
    expenditure = Expenditure.objects.get(pk=item_id)
    print(request.method, 'update')

    if request.method == 'GET':

        category_list = Category.objects.filter(uid=user)
        today = date.today().strftime("%Y-%m-%d")

        if user != expenditure.uid:
            messages.error(request, '조회권한이 없습니다.')

        e_serializer = ExpenditureSerializer(expenditure)
        context = {"category_list": category_list, "expenditure": e_serializer.data, "update": True, "today": today}
        return render(request, 'expenditure/update_item.html', context)

    elif request.method == 'POST':

        update_data = {
            'pay_date': request.POST.get('pay_date'),
            'cid': request.POST.get('category'),
            'product': request.POST.get('product'),
            'price': request.POST.get('price'),
            'place': request.POST.get('place'),
            'memo': request.POST.get('memo')
        }

        if user != expenditure.uid:
            messages.error(request, '수정권한이 없습니다.')

        e_serializer = ExpenditureSerializer(expenditure, data=update_data, partial=True)
        if e_serializer.is_valid(raise_exception=True):
            e_serializer.save()
            return redirect('expenditure:list')


@permission_classes([IsAuthenticated])
def delete_item(request, item_id):
    """
    내역 삭제
    :param request:
    :param item_id:
    :return:
    """
    user = request.user
    expenditure = get_object_or_404(Expenditure, pk=item_id)
    print('delete')
    if user != expenditure.uid:
        messages.error(request, '삭제권한이 없습니다.')

    expenditure.delete()
    return redirect('expenditure:list')
