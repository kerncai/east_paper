"""paper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include,url
from index.views import index, login_view, logout, login_historys, page_error, page_not_found, UserPasswordUpdateView
from django.conf.urls.static import static
from django.conf import settings


handler404 = page_not_found
handler500 = page_error


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('', index),
    path('index.html', index, name="index"),
    path('login.html', login_view),
    path('logout.html', logout,name="logout"),
    path('password_update.html',UserPasswordUpdateView.as_view() , name="password_update"),
    path('index/login-history.html', login_historys, name="login-history"),
    path('name/', include('name.urls', namespace="name", ), ),
    path('face/', include('face.urls', namespace="face", ), ),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # static and media
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
    urlpatterns.extend(
        staticfiles_urlpatterns()
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
 
    # debug toolbar
    import debug_toolbar
 
    urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))
