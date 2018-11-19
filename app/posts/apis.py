import json

from django.http import HttpResponse
from rest_framework import status, permissions
from rest_framework.exceptions import NotAuthenticated, APIException
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.serializers import PostSerializer, PostLikeSerializer
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
        serializer = PostLikeSerializer(
            data={**request.data, 'post': post_pk},
            context={'request': request},
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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
