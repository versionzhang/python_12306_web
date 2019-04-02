from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from .models import BasicConfig, PresaleConfig, TrainAccount, \
    AutoCodeAccount, EmailConfig, TotalConfig, BuyTasks, ProxyConfig


@admin.register(BasicConfig)
class BasicConfigAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(PresaleConfig)
class PresaleConfigAdmin(admin.ModelAdmin, DynamicArrayMixin):
    pass


@admin.register(TrainAccount)
class TrainAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(AutoCodeAccount)
class AutoCodeAccountAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailConfig)
class EmailConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(TotalConfig)
class TotalConfigAdmin(admin.ModelAdmin):
    pass


@admin.register(ProxyConfig)
class ProxyConfigAdmin(admin.ModelAdmin):
    pass

@admin.register(BuyTasks)
class BuyTasksAdmin(admin.ModelAdmin):
    pass
