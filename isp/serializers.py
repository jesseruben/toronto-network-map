from rest_framework import serializers
from .models import ISP, Plan

class PlanSerializer(serializers.ModelSerializer):
    isp = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Plan
        fields = ('isp', 'name', 'price', 'contract', 'contract_length', 'download_rate', 'upload_rate',
                  'bandwidth', 'bandwidth_limit', 'limited_offer', 'link')

class ISPSerializer(serializers.ModelSerializer):
    plans = PlanSerializer(many=True)

    class Meta:
        model = ISP
        fields = ('name', 'website', 'phone', 'support_phone', 'rating', 'facebook', 'twitter', 'support_link', 'plans')
