from django.conf.urls import url
from rest_framework import routers

from webadmin.views import BuyTaskViewSet

urlpatterns = [
]

router = routers.SimpleRouter()
router.register(r'tasks', BuyTaskViewSet)
urlpatterns += router.urls
