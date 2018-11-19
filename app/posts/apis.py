import json

from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import PostSerializer
from .models import HashTag, Post, PostLike


class PostList(APIView):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    # drf설치, settings에 적절히 설정 후 작업
    # Postman에서 테스트하기
    # URL: /api/posts/
    def get(self, request, format=None):
        # 모든 Post목록을 리턴
        posts = Post.objects.all()
        return Response(PostSerializer(posts, many=True).data)

    def post(self, request, format=None):
        # 새 Post를 생성
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    # URL: /api/posts/<pk>/
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise HTTP404

    def get(self, request, pk, format=None):
        # pk에 해당하는 Post정보를 리턴
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        return self.put(request, pk, format, partial=True)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeCreate(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, post_pk):
        # URL1: /posts/like/
        # URL2: /posts/<post_pk>/like/
        # 특정 Post에 대해서 request.user의
        # PostLike를 만든다
        #  조건: request.user와 해당 Post에 연결된 PostLike가 없어야 함
        post = get_object_or_404(Post, pk=post_pk)
        # 위 user, post와 연결된 PostLike가 있는지
        if PostLike.objects.filter(user=request.user, post=post).exists():
            data = {
                'detail': '이미 좋아요를 누른 포스트입니다',
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        post_like = PostLike.objects.create(user=request.user, post=post)
        return Response(status=status.HTTP_201_CREATED)


class PostLikeDelete:
    pass


def tag_search(request):
    # URL: '/posts/api/tag-search/'

    # request.GET으로 전달된
    #  search_keyword값을 가지는(contains)

    #  HashTag목록을 가져와 각 항목을 dict로 변경
    #   dict요소의 list로 만들어 HttpResponse에 리턴
    #  ex) [{}, {}, {}]
    keyword = request.GET.get('keyword')
    tags = []
    if keyword:
        tags = list(HashTag.objects.filter(name__istartswith=keyword).values())
    result = json.dumps(tags)
    return HttpResponse(result, content_type='application/json')
