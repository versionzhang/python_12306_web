from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import BasicConfig, PresaleConfig


@admin.register(BasicConfig)
class BasicConfigAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(PresaleConfig)
class PresaleConfigAdmin(admin.ModelAdmin, DynamicArrayMixin):

    class Meta:
        model = PresaleConfig
