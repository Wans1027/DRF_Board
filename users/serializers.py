import profile
from urllib.robotparser import RequestRate
from django.contrib.auth.models import User #User모델
from django.contrib.auth.password_validation import validate_password #패스워드검증도구

from rest_framework import serializers
from rest_framework.authtoken.models import Token #Token model
from rest_framework.validators import UniqueValidator #이메일 중복 방지를 위한 검증 도구
from django.contrib.auth import authenticate #유저인증
from .models import Profile

class RegisterSerializer(serializers.ModelSerializer):#회원가입 시리얼라이저
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset=User.objects.all())], #이메일 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], #비밀번호에 대한 검증
    )
    password2 = serializers.CharField(write_only=True, required=True)#비밀번호 확인을 위한 필드

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data): #추가적인 비밀번호 일치 여부 확인
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return data

    def create(self, validated_data): #CREATE요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함.
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    #write_only 옵션을 통해 클라이언트->서버 방향의 역직렬화는 가능, 서버-> 클라이언트 방향의 직렬화는 불가능

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user) #토큰에서 유저찾아 응답
            return token
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."}
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profile
        fields = ("nickname", "position", "subjects", "image")




        


