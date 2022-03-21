from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
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
            user = serializer.save()
            login(request, user)
            return redirect('home')

        return redirect('common:signup', error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'index.html')


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile(request, profile_id):
    """
    개인 프로필 보기/수정
    :param profile_id: user 레코드 아이디
    :param request: 수정할 데이터
    :return:
    """
    if request.method == 'GET':
        return render(request, 'common/profile.html')
    else:
        user = get_object_or_404(User, pk=profile_id)
        # pariail=True를 Serializer 생성에 추가하면 부분적인 .update를 허용하게 되고,
        # 유효성 검사에서 수정하고자 하는 부분만 유효성 검사를 하게 된다.
        serializer = RegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            # .save()는 해당 인스턴스가 데이터 베이스가 존재하는 경우, update 함수를 사용하여 인스턴스를 업데이트한다.
            serializer.save()
            return redirect('common:profile', profile_id=user.id)

        return redirect('common:profile', error=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
