from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from webadmin.models import PresaleConfig, BasicConfig, AutoCodeAccount, \
    TrainAccount, EmailConfig, TotalConfig, BuyTasks


class PresaleConfigSerializers(ModelSerializer):
    class Meta:
        model = PresaleConfig
        exclude = ('c_time', 'm_time', 'name')


class BasicConfigSerializers(ModelSerializer):
    station_groups = serializers.SerializerMethodField('convert_station_groups', source='station_groups')

    def convert_station_groups(self, obj):
        return [{"from_station": v.split(',')[0], "to_station": v.split(',')[1] } for v in obj.station_groups]

    class Meta:
        model = BasicConfig
        exclude = ('c_time', 'm_time', 'name')

class AutoCodeAccountSerializers(ModelSerializer):
    class Meta:
        model = AutoCodeAccount
        exclude = ('c_time', 'm_time', 'name')

class TrainAccountSerializers(ModelSerializer):
    class Meta:
        model = TrainAccount
        exclude = ('c_time', 'm_time', 'name')


class EmailConfigSerializers(ModelSerializer):
    class Meta:
        model = EmailConfig
        exclude = ('c_time', 'm_time', 'name')

class TotalConfigSerializers(ModelSerializer):
    presale_config = PresaleConfigSerializers(required=False)
    basic_config = BasicConfigSerializers()
    train_account = TrainAccountSerializers()
    auto_code_account_ruokuai = AutoCodeAccountSerializers(required=False, source='auto_code_account')
    email_config = EmailConfigSerializers(required=False)

    class Meta:
        model = TotalConfig
        exclude = ('c_time', 'm_time', 'name')


class BuyTasksSerializers(ModelSerializer):
    config = TotalConfigSerializers()
    proxy = serializers.SerializerMethodField('get_proxy_url', source='proxy')
    log = serializers.SerializerMethodField('get_log_string')

    class Meta:
        model = BuyTasks
        fields = "__all__"

    def get_log_string(self, instance):
        return ""

    def get_proxy_url(self, obj):
        if obj.proxy:
            return obj.proxy.proxy_url
        else:
            return ''
