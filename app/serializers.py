from rest_framework import serializers
from app.models import MyUser,Item


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['email','password',]
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def create(self,validate_data):
        return MyUser.objects.create_user(**validate_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=['email','password']
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']        