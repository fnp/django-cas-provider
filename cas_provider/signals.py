"""cas_provider.signals -- signal definitions for cas_provider
"""
from django import dispatch


on_cas_collect_histories = dispatch.Signal()

on_cas_login = dispatch.Signal()

on_cas_login_success = dispatch.Signal()

cas_collect_custom_attributes = dispatch.Signal()
