# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

urlpatterns = [

	url(r'^home$', Home.as_view(), name="place_order"),

]
