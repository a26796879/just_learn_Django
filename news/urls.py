from news.viewsets import NewsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', NewsViewSet, basename='news')
urlpatterns = router.urls