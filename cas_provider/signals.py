# -*- coding: utf-8 -*-
"""cas_provider.signals -- signal definitions for cas_provider
"""
from __future__ import unicode_literals

from django import dispatch


on_cas_collect_histories = dispatch.Signal(providing_args=["for_email"])

on_cas_login = dispatch.Signal(providing_args=["request"])

on_cas_login_success = dispatch.Signal(providing_args=["user", "service"])

cas_collect_custom_attributes = dispatch.Signal(providing_args=['user'])
