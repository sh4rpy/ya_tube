from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


handler404 = "posts.views.page_not_found"
handler500 = "posts.views.server_error"

urlpatterns = [
    # раздел авторизации
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    # раздел администратора
    path('admin/', admin.site.urls),
    # flatpages
    path("about/", include("django.contrib.flatpages.urls")),
    path('about-author/', views.flatpage,
         {'url': '/about-author/'}, name='about_author'),
    path('about-spec/', views.flatpage,
         {'url': '/about-spec/'}, name='about_spec'),
    # import из приложения posts
    path('', include('posts.urls')),
    # api
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
