from rest_framework import serializers
from contact.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    subject = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    message = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Contact
        # each field in the fields tuple is required, and some fields shouldn't be available
        fields = ('subject', 'email', 'message')

    def create(self, validated_data):
        """
        this is deserialization function to create tuples out of JSON
        :param validated_data:
        :return:
        """
        return Contact.objects.create(**validated_data)