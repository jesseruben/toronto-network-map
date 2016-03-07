from rest_framework import serializers


class NDTRegionalSmall(serializers.Serializer):
    id = serializers.FloatField()
    download_rate = serializers.FloatField()
    upload_rate = serializers.FloatField()
    price = serializers.FloatField()
    location = serializers.CharField()
    isp_name = serializers.CharField()
    isp = serializers.FloatField()
