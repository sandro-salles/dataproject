from django.conf.urls import include, patterns, url
from django.contrib import admin
from person.views import PersonList, PersonDetail, PersonCount
from person.contact.views import CarrierList, AddressCityNeighborhoodList, AddressCityList, PhoneAreacodeList
from account.views import CorporationDetail
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),


    url(r'^account/corporation/(?P<pk>[0-9]+)/$',
        CorporationDetail.as_view(), name='corporation-detail'),

    url(r'^contact/phone/carrier/$', CarrierList.as_view(), name='phone-carrier-list'),
    url(r'^contact/phone/areacode/$', PhoneAreacodeList.as_view(), name='phone-areacode-list'),
    url(r'^contact/address/city-neighborhood/$', AddressCityNeighborhoodList.as_view(), name='address-city-neighborhood-list'),
    url(r'^contact/address/city/$', AddressCityList.as_view(), name='address-city-list'),

    url(r'^person/count/$', PersonCount.as_view(), name='person-count'),

    url(r'^person/$', PersonList.as_view(), name='person-list'),
    url(r'^person/(?P<pk>[0-9]+)/$',
        PersonDetail.as_view(), name='person-detail'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
