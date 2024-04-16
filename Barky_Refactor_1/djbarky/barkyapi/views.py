from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bookmark, Snippet
from .permissions import IsOwnerOrReadOnly
from .serializers import BookmarkSerializer, SnippetSerializer, UserSerializer

from rest_framework import filters #add

# Create your views here.
class BookmarkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookmarks to be viewed or edited.
    """

    queryset = Bookmark.objects.all().order_by("-date_added")
    serializer_class = BookmarkSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'title', 'url', 'date_added']
    


class UserViewSet(viewsets.ModelViewSet):
    #change ReadOnlyModelViewSet to ModelViewSet
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly] #add



class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'title', 'url', 'date_added']
    
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
