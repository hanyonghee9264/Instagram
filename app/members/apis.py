from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer, AuthTokenSerializer

User = get_user_model()


class AuthTokenView(APIView):
    """
    username, password를 받아서
    사용자 인증에 성공하면 해당 사용자와 연결된 토큰 정보와 사용자 정보를 동시에 리턴
    """

    def post(self, request):
        # URL: /members/auth-token/
        # 사용자 인증정보가 와야지만 사용 가능
        #  -> 없다면 만들어주고, 있다면 기존에 있던 Token을 사용
        # 돌려주는 데이터는

        # request.data로 오는 데이터는 'username', 'password'
        #  그냥 Serializer (ModelSerializer아님)
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            # to_representation() 함수를 Serializer내에 정의
            # -> {'token': <Token key>, 'user': <해당 유저 정보 serialize>}
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    def get(self, request, pk=None):
        # URL1: /apis/members/view/<int:pk>/
        # URL2: /apis/members/view/profile/
        if pk:
            user = get_object_or_404(User, pk=pk)
        else:
            user = request.user
            if not user.is_authenticated:
                raise NotAuthenticated()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserDetail(generics.RetrieveAPIView):
    # URL1: apis/members/<int:pk>/
    # URL2: apis/members/profile/
    #  2개의 URL에 모두 매칭되도록

    # generics.GenericAPIView를 참고해서
    #  get_object() 메서드를 적절히 오버라이드
    #   pk값이 주어지면 pk에 해당하는 User를 리턴 (기본값)
    #   pk값이 주어지지 않았다면 request.user에 해당하는 User를 리턴
    #   pk값이 주어지지 않았는데 request.user가 인증되지 않았다면 예외 일으키기

    # 돌려주는 데이터는 유저정보 serialize결과
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_object(self):
        # 하나의 Object를 특정화 하기 위한 조건을 가진 필드명 또는 URL패턴명
        #  기본값: 'pk'
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        # 'pk'가 URL패턴명 중에 없으면
        if lookup_url_kwarg not in self.kwargs:
            # 근데 인증된 상태도 아니라면
            if not self.request.user.is_authenticated:
                raise NotAuthenticated()
            return self.request.user

        # 'pk'가 URL패턴명에 있으면,
        # 기존 GenericAPIView에서의 동작을 그대로 실행
        return super().get_object()
