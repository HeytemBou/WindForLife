# rest framework imports
from rest_framework.routers import DefaultRouter

# Django imports
from django.urls import path, include

from  apps.accounts.api.v1.viewsets import AccountsViewSet

############################## Router for User Management API ##############################

router = DefaultRouter(trailing_slash=False)
router.register('accounts', AccountsViewSet, basename='accounts')



urlpatterns = [
    path('', include(router.urls)),
]
