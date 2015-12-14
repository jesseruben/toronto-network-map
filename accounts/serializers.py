from rest_framework import serializers
from accounts.models import User
from accounts.models import UserUID
import logging
import re

logger = logging.getLogger(__name__)


def password_validator(value):
    regex = '^(?=.*[a-z])(?=.*[A-Z]){8,}(?=.*\d).+$'
    if len(value) < 8 or len(value) > 24 or not re.match(regex, value):
            raise serializers.ValidationError('This field should at least contain one small letter, '
                                              'one capital letter, one digit and minimum length of 8')


def username_validator(value):
    regex = '^[a-zA-Z0-9_]*$'
    if not re.match(regex, value):
        raise serializers.ValidationError('This field should only contain characters and numbers.')


class UserSerializer(serializers.ModelSerializer):
    # these are added here to impose required False and the hash password cannot be queried by get
    email = serializers.EmailField(required=True, max_length=255)
    username = serializers.CharField(required=True, max_length=10, min_length=5, validators=[username_validator])
    password = serializers.CharField(write_only=True, required=True, validators=[password_validator])
    confirm_password = serializers.CharField(write_only=True, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        # each field in the fields t uple is required, and some fields shouldn't be available
        # to the user due to security reason , i.e. is_active
        fields = ('email', 'username', 'created_at', 'updated_at',
                  'password', 'confirm_password', 'log_guid')
        read_only_fields = ('created_at', 'updated_at', 'log_guid')

    def create(self, validated_data):
        """
        this is deserialization function to create tuples out of JSON
        :param validated_data:
        :return:
        """
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        When a user's password is updated, their session account hash must be explicitly updated.
        If we don't do this here, the user will not be authenticated on their next request
        and will have to log in again.
        update_session_auth_hash(self.context.get('request'), instance)
        """
        password = validated_data.get('password', None)
        instance.set_password(password)
        instance.save()
        return instance

    def validate(self, attrs):
        password = attrs.get('password', None)
        confirm_password = attrs.get('confirm_password', None)

        if password and confirm_password and (password != confirm_password):
            raise serializers.ValidationError('Password and confirm password do not match')
        return attrs


# This serializer is used in the updatepasswordview and setpasswordview to check that newpass and confrmpass are same
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[password_validator])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        # TODO : Add more type of the accounts along with it's response to the frontend
        new_password = attrs.get('new_password', None)
        confirm_password = attrs.get('confirm_password', None)

        if not new_password or not confirm_password:
            raise serializers.ValidationError('Password and confirm password are both required.')

        if new_password and confirm_password and (new_password != confirm_password):
            raise serializers.ValidationError('New Password and Confirm Password do not match.')
        else:
            return attrs


class UserUIDSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserUID
        # each field in the fields tuple is required, and some fields shouldn't be available
        # to the user due to security reason , i.e. is_active
        fields = ('guid', 'user', 'expiration_date')

    def create(self, validated_data):
        """
        this is deserialization function to create tuples out of JSON
        :param validated_data:
        :return:
        """
        return UserUID.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.guid = validated_data.get('guid', instance.guid)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.save()
        return instance
