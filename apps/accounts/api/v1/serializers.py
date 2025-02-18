# validators
from django.contrib.auth.password_validation import validate_password
from apps.accounts.api.v1.validators import custom_validate_password, validate_email

# Rest Framework imports
from rest_framework import serializers

# Django imports
from django.contrib.auth import get_user_model

# get the user model
Account = get_user_model()


##########################################
##### SIGN UP SERIALIZER #################
##########################################

class AccountSignUpSerializer(serializers.Serializer):
    """
    Serializer for main account sign Up
    """

    # Fields to create the account
    password = serializers.CharField(write_only=True, 
                                     style={'input_type': 'password'},
                                     required=True,
                                     validators=[custom_validate_password, validate_password])
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    email = serializers.EmailField(required=True, validators=[validate_email])

   
    def validate(self, data):
        # Check that the two password entries match
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError("PASSWORDS_DO_NOT_MATCH")
        return data

    def create(self, validated_data):
        # Remove the password_confirm field. we don't need it anymore
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')

        # Create the account
        account = Account(
            email=validated_data.get('email'),
        )
        account.set_password(password)
        account.save()

        return account


##########################################
##### SIGN IN SERIALIZER #################
##########################################
class AccountSignInSerializer(serializers.Serializer):
    """
    Serializer for main account sign in
    """
    email = serializers.EmailField(required=True, validators=[validate_email])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, data):
        """
        Verify that both the mail and the password are not empty, and that no other fields are included
        """
        if len(data) > 2:
            raise serializers.ValidationError("INVALID_FIELDS")
        return data