from news.viewsets import NewsViewSet,UserViewSet,GroupViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', NewsViewSet, basename='news')
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
urlpatterns = router.urls
