from posts.models import Post, Comment, Group, Follow, User
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'title', 'description', 'slug')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(),
    )

    class Meta:
        fields = ('id', 'user', 'following')
        model = Follow

    def validate_following(self, value):
        current_user = self.context['request'].user
        if Follow.objects.filter(user=current_user, following=value).exists():
            raise serializers.ValidationError(
                f"You are already subscribed to {value}"
            )
        elif current_user == value:
            raise serializers.ValidationError(
                "You can't subscribe to yourself"
            )
        return value
