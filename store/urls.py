from django.contrib import admin
from django.urls import include, path,include
from products.views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name='index'),
    path('products/',include("products.urls",namespace='products')),
    path('users/',include("users.urls",namespace='users')),
    path('',include("news.urls",namespace='news')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)