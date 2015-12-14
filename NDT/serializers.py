from .models import NDT, NDTProfile, Server, Web100
from rest_framework import serializers


class NDTSerializer(serializers.ModelSerializer):
    class Meta:
        model = NDT
        fields = ('download_rate', 'upload_rate', 'latency', 'ndt_profile', 'nominal_download_rate', 'rating_general',
                  'nominal_upload_rate', 'latitude', 'longitude', 'bandwidth', 'price', 'city', 'country', 'isp_name')


class NDTSerializerSmall(serializers.ModelSerializer):
    class Meta:
        model = NDT
        fields = ('id', 'latitude', 'longitude', 'download_rate', 'upload_rate', 'isp_name', 'rating_general', 'price')

    def create(self, validated_data):
        return NDT.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.upload_rate = (instance.upload_rate*float(instance.average_index) +
                                float(validated_data.get('upload_rate', None)))/float(instance.average_index+1)
        instance.download_rate = (instance.download_rate*float(instance.average_index) +
                                  float(validated_data.get('download_rate', None)))/float(instance.average_index+1)
        instance.average_index += 1
        instance.save()
        return instance


class NDTProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NDTProfile
        fields = ('latitude', 'longitude', 'nominal_download_rate', 'nominal_upload_rate', 'bandwidth', 'price',
                  'contract', 'service_type', 'vpn', 'name', 'rating_general', 'rating_customer_service', 'country',
                  'province', 'city', 'promotion', 'isp')
        extra_kwargs = {
            'user': {
                'write_only': True,
            },
        }


class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields = ('name', 'country', 'url')


class NDTProfileSerializerSmall(serializers.ModelSerializer):
    """
    This serializer is used for the list and retrieve so the user does not see all the details"
    """
    class Meta:
        model = NDTProfile
        fields = ('name', 'service_type')


class Web100Serializer(serializers.ModelSerializer):
    class Meta:
        model = Web100
        fields = ('blob', 'ndt')
