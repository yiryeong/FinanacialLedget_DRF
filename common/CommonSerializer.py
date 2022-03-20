from rest_framework import serializers
from django.contrib.auth.models import User


# registration
class RegistrationSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(
    #     max_length=100,
    #     style={'input_type': 'username', 'placeholder': '사용자 아이디', 'autofocus': True}
    # )
    # password = serializers.CharField(
    #     max_length=100,
    #     style={'input_type': 'password', 'placeholder': '비밀번호'}
    # )
    # email = serializers.EmailField(
    #     max_length=100,
    #     style={'input_type': 'Email', 'placeholder': '이메일'}
    # )
    password2 = serializers.CharField(
        style={'input_type': 'password', 'placeholder': '비민번호 확인'},
        write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "password", 'password2', 'email']
        # 비밀번호는 보안상 암호화가 되었다 하더라도 클라이언트 측에 전달하지 못하게 하기 위해 write_only를 사용
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        account = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        account.set_password(password)
        account.save()
        return account

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance

