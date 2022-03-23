from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Category
from .CategorySerializer import CategorySerializer


@permission_classes([IsAuthenticated])
def category(request):
    """
    카테고리 전체 조회 / 등록
    :param request:
    :return:
    """
    if request.method == 'GET':
        user = request.user
        category_list = Category.objects.filter(uid=user)

        # page = request.GET.get('page', '1')
        category_name = request.GET.get('search_category', '')

        if category_name:
            category_list = category_list.filter(Q(category_name__icontains=category_name)).distinct()

        serializer = CategorySerializer(category_list, many=True)
        # # paging
        # paginator = Paginator(category_list, 10)  # 페이지당 10개씩 보여 주기
        # page_obj = paginator.get_page(page)

        return render(request, 'category/list.html', {'category_list': serializer.data, 'search_category': category_name})
    elif request.method == 'POST':
        user_id = request.user.id
        category_info = {
            'category_name': request.POST['add_category'],
            'uid': user_id,
        }
        serializer = CategorySerializer(data=category_info)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('category:list')


@permission_classes([IsAuthenticated])
def category_modify(request, category_id):
    """
    특정 카테고리 수정
    :param category_id: 카테고리 레코드 아이디
    :param request:
    :return:
    """
    category = get_object_or_404(Category, pk=category_id)

    if request.user != category.uid:
        messages.error(request, '수정권한이 없습니다.')
    else:
        data = {
            'category_name': request.POST['change_category']
        }

        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('category:list')


@permission_classes([IsAuthenticated])
def category_delete(request, category_id):
    """
    특정 카테고리 삭제
    :param category_id: 카테고리 레코드 아이디
    :param request:
    :return:
    """
    category = get_object_or_404(Category, pk=category_id)

    if request.user != category.uid:
        messages.error(request, '삭제권한이 없습니다.')
    else:
        category.delete()
    return redirect('category:list')
