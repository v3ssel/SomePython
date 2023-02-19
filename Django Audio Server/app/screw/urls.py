from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('files_list', views.files_list, name='files_list')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

