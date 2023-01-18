from rest_framework import generics, views
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# from .mixins import NewsStatusMixin, CommentStatusMixin, StatusMixin
from .models import News, NewsStatus, Comment, CommentStatus, Status
from .permissions import IsAuthorPermission
from .serializers import NewsSerializer, CommentSerializer, CommentStatusSerializer, StatusSerializer, \
    NewsStatusSerializer


class NewsNumberPagination(PageNumberPagination):
    page_size = 1



class NewsListCreateAPIView(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthorPermission, ]
    pagination_class = NewsNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title', ]
    ordering_fields = ['created', ]



    def perform_create(self, serializer):
        serializer.save(author=self.request.user.author)


class NewsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(news_id=self.kwargs.get('news_id'))

    def perform_create(self, serializer):
        serializer.save(
            news_id=self.kwargs.get('news_id'),
            author=self.request.user.author
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        super().get_queryset().filter(comment_id=self.kwargs.get('comment_id'))


class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        super().get_queryset().filter(status_id=self.kwargs.get('status_id'))





class StatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        super().get_queryset().filter(status_id=self.kwargs.get('status_id'))


class NewsStatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = NewsStatusSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(
            news_status_id=self.kwargs.get('news_status_id'))

    def post(self, request, *args, **kwargs):
        news_id = kwargs.get('news_id')
        author = request.user
        status = kwargs.get('status')
        new_status = Status(
            news_id=news_id,
            author=author,
            status=status
        )
        new_status.save()
        return Response(status=200)


class CommentStatusRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentStatus.objects.all()
    serializer_class = CommentStatusSerializer
    permission_classes = [IsAuthorPermission, ]

    def get_queryset(self):
        return super().get_queryset().filter(
            comment_status_id=self.kwargs.get('comment_status_id'))

    def post(self, request, *args, **kwargs):
        comment_id = kwargs.get('comment_id')
        author = request.user
        status = kwargs.get('status')
        new_status = Status(
            news_id=comment_id,
            author=author,
            status=status
        )
        new_status.save()
        return Response(status=200)

class StatusNewsCreateAPI(views.APIView):
    def get(self, request, *args, **kwargs):
        news = News.objects.get(id=kwargs.get('news_id'))
        status = Status.objects.get(slug=kwargs.get('slug'))
        new_status = NewsStatus.objects.create(
            status=status,
            author=request.user.author
        )
        return Response(data={'message':'Status added'}, status=201)