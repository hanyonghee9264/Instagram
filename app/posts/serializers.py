from rest_framework import serializers

from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    # 내가 이 Serializer에 주어진 'Post'에
    # 좋아요를 눌렀는지 여부를
    # is_like 필드에 추가

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'photo',
            'created_at',
            'is_like',
        )
        read_only_fields = (
            'author',
        )

    def get_is_like(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                postlike = obj.postlike_set.get(user=user)
                return PostLikeSerializer(postlike).data
            except PostLike.DoesNotExist:
                return


class PostLikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = PostLike
        fields = (
            'pk',
            'post',
            'user',
            'created_at',
        )
        read_only_fields = (
            'user',
        )
