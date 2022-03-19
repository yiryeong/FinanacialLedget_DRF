from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from common.CommonSerializer import RegistrationSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    회원가입
    :param request: username, password, password2, email
    :return:
    """
    if request.method == 'GET':
        return render(request, 'common/signup.html')
        # # modelForm 처럼 회원가입 form 생성
        # serializer = RegistrationSerializer()
        # return render(request, 'common/signup1.html', {'serializer': serializer})
    else:
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.save()
            login(request, user)
            return redirect('home')

        return redirect('common:signup', error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')
