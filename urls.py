from django.urls import path

# from . import httpCloudService
from . import httpCldSrvc

urlpatterns = [
    # path("receive/", httpCloudService.receive_vps_http_request),
    path("search_available_vps/", httpCldSrvc.search_available_vps),
    path("vps_update_status/", httpCldSrvc.vps_update_status),
    path("vps_register/", httpCldSrvc.vps_register)
]