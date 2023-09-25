from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views
from api.views import PostViewSet, GroupViewSet, CommentViewSet

app_name = 'api'

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
