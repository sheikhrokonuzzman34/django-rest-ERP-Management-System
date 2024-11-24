from rest_framework import serializers
from apps.accounts.models import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'role', 'department', 'division', 'salary']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is not returned in the response
        }

    def create(self, validated_data):
        """
        This method handles creating a new user from the validated data.
        It hashes the password before saving it to the database.
        """
        # Extract the password
        password = validated_data.pop('password', None)
        
        # Create a new CustomUser instance
        user = CustomUser(**validated_data)

        # Set the password (this will hash it)
        if password:
            user.set_password(password)

        # Save the user instance to the database
        user.save()

        return user
    
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)    
