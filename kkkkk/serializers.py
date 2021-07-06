from django.contrib.postgres import serializers
from rest_framework import serializers
from rest_framework.authtoken.admin import User
from rest_framework.exceptions import ValidationError

from kkkkk.models import Post, Comment, PostLike


class PostListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "id created_date title text comments count is_like like_count".split()

    def get_comments(self, instance):
        comment = Comment.objects.filter(post_id=instance)
        return CommentListSerializer(comment, many=True).data

    def get_count(self, instance):
        return Comment.objects.filter(post=instance).count()

    def get_is_like(self, instance):
        if PostLike.objects.filter(post=instance,
                                   user=self.context['request'].user).count():
            return True
        return False

    def get_like_count(self, instance):
        return PostLike.objects.filter(post=instance).count()


class PostValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=2, max_length=100)
    text = serializers.CharField(min_length=5)

    def validate(self, object):
        object = object["title"]
        if Post.objects.filter(title=object).count() > 0:
            raise ValidationError("Takoi post sushestvuet")
        else:
            return object


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = 'id text'.split()


class CommentValidateSerializer(serializers.Serializer):
    comment = serializers.CharField(min_length=2, max_length=100)

    def validate_comment(self, object):
        if Comment.objects.filter(name=object).count() > 0:
            raise ValidationError("Takoi comment uje est")
        else:
            return object


class UserLoginValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class UserRegisterValidateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    password1 = serializers.CharField(max_length=100)

    def validate(self, object):
        if User.object.filter(username=object['username']).count() > 0:
            raise ValidationError("Takoi user uje est")
        else:
            if object['password'] != object['password1']:
                raise ValidationError("Paroli ne sovpadayt")
            return object
