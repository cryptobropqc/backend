"""
URL configuration for CryptoBro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from django.conf import settings
from django.conf.urls.static import static
from . import views

sitemaps = {
'posts': PostSitemap,
}

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('admsys/', admin.site.urls),
    path('api_cryptobro/', include('api_cryptobro.urls', namespace='api_cryptobro')),
    path('', views.index, name='index'),
    path('account/', include('account.urls', namespace='account')),
    path('account/', include('django.contrib.auth.urls')),
    # path('blog/', include('blog.urls', namespace='blog')),
    path('blog/', views.blog, name='blog'),
    path('faq/', views.faq, name='faq'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('account/', include('account.urls')),
    # path('', views.index, name='index'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
