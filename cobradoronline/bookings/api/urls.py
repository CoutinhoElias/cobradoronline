from django.conf.urls import url

app_name = 'bookings-api'

from .views import (
    PostListAPIView,
    PostListFeriadoAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView,
    PostList2APIView, PostUpdate2APIView)

urlpatterns = [
    url(r'^$', PostListAPIView.as_view(), name='listapi'),
    url(r'^(?P<pk>\d+)/$',PostDetailAPIView.as_view(),name='detail'),
    url(r'^(?P<pk>\d+)/delete/$',PostDeleteAPIView.as_view(),name='delete'),
    url(r'^(?P<pk>\d+)/edit/$',PostUpdateAPIView.as_view(),name='update'),
    url(r'^create/$', PostCreateAPIView.as_view(), name='create'),
    url(r'^feriado/$', PostListFeriadoAPIView.as_view(), name='feriado'),
    #url(r'^(?P<slug>[\W-]+)/$',PostDetailAPIView.as_view(),name='detail')

    url(r'^list/$', PostList2APIView.as_view(), name='listapi2'),
        url(r'^(?P<pk>\d+)/edita/$', PostUpdate2APIView.as_view(), name='update2'),
]