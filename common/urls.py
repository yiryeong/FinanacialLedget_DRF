from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'common'

urlpatterns = [
    # django.contrib.auth 앱의 LoginView 클래스를 활용 했으므로 별도의 views.py 파일 수정이 필요 없음!
    # LoginView는 registration/login.html 를 기본으로 호출한다. 아래처런 설정하여 common/login.html 호출하도록 변경
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]
