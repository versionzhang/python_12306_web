from rest_framework.serializers import ModelSerializer

from webadmin.models import PresaleConfig


class PresaleConfigSerializers(ModelSerializer):
    class Meta:
        model = PresaleConfig
        fields = "__all__"
