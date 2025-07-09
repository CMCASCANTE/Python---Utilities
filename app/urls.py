from django.urls import path

from app.vistas import api
from app.vistas import telnet
from app.vistas import dnsChecker
from app.vistas import bklChecker
from app.vistas import index


urlpatterns = [
    #path("", views.index, name="index"),
    path("", index.index, name="index"),
    path("dns", dnsChecker.dnsChecker, name="dnsChecker"),
    path("telnet", telnet.telnet, name="telnet"),
    path("bkl", bklChecker.bklChecker, name="bklChecker"),
    path("api", api.api, name="api"),
]