from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


@permission_classes([IsAuthenticated])
def day_report(request):
    return render(request, 'report/list.html', {"select_week": True})


@permission_classes([IsAuthenticated])
def week_report(request):
    return render(request, 'report/list.html')
