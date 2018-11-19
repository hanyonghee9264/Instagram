from rest_framework import serializers

from members.models import User

from .models import Post, Comment, PostLike


class PostSerializer(serializers.ModelSerializer):
    # 작성자
    # 댓글목록
    # 좋아요 누른 사람 목록
    class Meta:
        model = Post
        fields = (
            'author',
            'photo',
            'created_at',
        )
        read_only_fields = (
            'author',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'img_profile',
            'site',
            'introduce',
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'post',
            'author',
            'content',
        )


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = (
            'post',
            'user',
            'created_at'
        )
