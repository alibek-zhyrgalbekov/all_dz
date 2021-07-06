from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from kkkkk.models import Post, Comment, PostLike
from rest_framework.response import Response
from kkkkk.serializers import PostListSerializer, CommentListSerializer, CommentValidateSerializer, \
    PostValidateSerializer, UserLoginValidateSerializer, UserRegisterValidateSerializer


@api_view(['GET', 'POST'])
def post_list_views(request):
    if request.method == "POST":

        serializer = PostValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'errors': serializer.errors
                }
            )
        post = Post.objects.create(title=request.data["title"], text=request.data["text"],
                                   is_like=request.data["is_like"])
        return Response(data={'message': 'created'})
    else:
        posts = Post.objects.all()
        data = PostListSerializer(posts, many=True, context={"request": request}).data
        return Response(data={'list': data})


@api_view(['GET'])
def post_item_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        raise NotFound('NETU')
    if request.method == 'GET':
        data = PostListSerializer(post, many=False).data
        return Response(data=data)
    elif request.method == 'POST':
        PostLike.objects.create(product=post,
                                user=request.user)
        return Response(data={'message': 'Product added to favourite'})


@api_view(['GET'])
def comment_list_view(request):
    comment = Comment.objects.all()
    data = CommentListSerializer(comment, many=True).data
    return Response(data={'list': data})


@api_view(['GET', 'POST'])
def comment_item_view(request, id):
    if request.method == "POST":

        serializer = CommentValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'errors': serializer.errors
                }
            )
        post = Post.objects.get(id=id)
        text = request.data.get('comment', '')
        Comment.objects.create(text=text, post_id=post.id)
        return Response(data={'message': 'created'})
    else:
        try:
            comment = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound('Ни-фи-га')
        data = CommentListSerializer(comment, many=False).data
        return Response(data=data)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':

        serializer = UserLoginValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'message': 'ERROR',
                    'errors': serializer.errors
                }
            )
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            token = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})
        else:
            return Response(data={'message': 'USER NOT FOUND'})


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserRegisterValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    'massage': "error",
                    'errors': serializer.errors
                }
            )
        User.objects.create_user(
            username=request.data['username'],
            email='a@n.ru',
            password=request.data['password']
        )
        return Response(data={'User created'})
