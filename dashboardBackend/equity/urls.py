from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import get_shares

urlpatterns = {
	path('', get_shares, name="shares"),
}

urlpatterns = format_suffix_patterns(urlpatterns)