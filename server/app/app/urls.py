from django.conf.urls import include, patterns, url
from django.contrib import admin
from person.views import PersonList, PersonDetail
from materialized.views import CarrierList, AreacodeList, CityList, NeighborhoodList, PersonCount
from account.views import CorporationDetail
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),


    url(r'^account/corporation/(?P<pk>[0-9]+)/$',
        CorporationDetail.as_view(), name='corporation-detail'),

    url(r'^filter/carrier/$', CarrierList.as_view(), name='filter-carrier-list'),
    url(r'^filter/areacode/$', AreacodeList.as_view(), name='filter-areacode-list'),
    url(r'^filter/city/$', CityList.as_view(), name='filter-city-list'),
    url(r'^filter/neighborhood/$', NeighborhoodList.as_view(), name='filter-neighborhood-list'),
    url(r'^filter/person/count/$', PersonCount.as_view(), name='filter-person-count'),

    url(r'^person/$', PersonList.as_view(), name='person-list'),
    url(r'^person/(?P<pk>[0-9]+)/$',
        PersonDetail.as_view(), name='person-detail'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )