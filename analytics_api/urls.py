"""analytics_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from api_demo_1 import views as api_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^battalion/$', api_views.BattalionView.as_view({
        'get':'list'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/$', api_views.BattalionView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/$', api_views.PostView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/$', api_views.MorchaView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/day/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.MorchaDayView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.MorchaWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^morcha/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.MorchaMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/recent/$', api_views.PostRecentView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/day/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.PostDayView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.PostWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^post/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.PostMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/recent/$', api_views.BattalionRecentView.as_view({
        'get': 'retrieve'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.BattalionWeekView.as_view({
        'get': 'retrieve'
    })),
    url(r'^battalion/(?P<pk>[0-9a-z-]+)/month/(?P<date>\d{4}-\d{2}-\d{2})/$', api_views.BattalionMonthView.as_view({
        'get': 'retrieve'
    })),
    url(r'^dashboard/battalion/$', api_views.BattalionDashboardView.as_view({
        'get': 'retrieve'
    })),
    url(r'^insert/$', api_views.insert),
    url(r'^test/$', api_views.test)
]




# url(r'^morcha/(?P<pk>[0-9a-z-]+)/week/(?P<date>\d{4}-\d{2}-\d{2})/', api_views.MorchaWeekView.as_view({
#     'get': 'retrieve'
# })),
# url(r'^posts/$', api_views.PostView.as_view({
#     'get': 'list'
# })),
# url(r'^test/$', api_views.Test.as_view({
#     'get': 'list'
# }))