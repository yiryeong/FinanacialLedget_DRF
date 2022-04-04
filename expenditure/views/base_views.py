from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from category.models import Category
from ..models import Expenditure
from ..ExpenditureSerializer import ExpenditureSerializer
from datetime import date, datetime, timedelta


@permission_classes([IsAuthenticated])
def expenditure(request):
    """
    결제정보 조회
    :param request:
    :return:
    """
    if request.method == 'GET':
        user = request.user
        category_list = Category.objects.filter(uid=user)
        today = date.today().strftime("%Y-%m-%d")

        # page = request.GET.get('page', '1')
        search_date = request.GET.get('search_date', today)
        kw = request.GET.get('kw', '')
        selected_category = request.GET.get('selected_category', '0')
        date_scope = int(request.GET.get('date_scope', '7'))

        end_date = datetime.strptime(search_date, "%Y-%m-%d")
        start_date = end_date - timedelta(days=date_scope)

        expenditure_list = Expenditure.objects.filter(uid=user, pay_date__range=[start_date, search_date])

        if selected_category != '0':
            expenditure_list = expenditure_list.filter(
                Q(cid=selected_category)
            )

        if kw:
            expenditure_list = expenditure_list.filter(
                Q(product__icontains=kw) |
                Q(memo__icontains=kw) |
                Q(price__icontains=kw) |
                Q(place__icontains=kw)
            )

        serializer = ExpenditureSerializer(expenditure_list, many=True)

        for data in serializer.data:
            data['category'] = category_list.get(id=data['cid']).name

        # # paging
        # paginator = Paginator(expenditure_list, 10)  # 페이지당 10개씩 보여 주기
        # page_obj = paginator.get_page(page)

        context = {'expenditure_list': serializer.data, 'category_list': category_list, "selected_category": int(selected_category), "search_date": search_date, "date_scope": date_scope, "kw": kw}
        return render(request, 'expenditure/list.html', context)
