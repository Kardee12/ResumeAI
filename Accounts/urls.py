from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from Accounts import views

urlpatterns = [
                  path('', include('allauth.urls')),
                  path('', include('allauth.socialaccount.urls')),
                  path('setup/', views.setup_view, name='setup'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
