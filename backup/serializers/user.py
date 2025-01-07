from rest_framework import serializers
from ..models.user import User
from .repository import RepositorySerializer

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'github_url']

class BackupUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username']
        
class FetchUserSerializer(serializers.ModelSerializer):
    repositories = RepositorySerializer(many=True, read_only=True)
    username = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'github_url', 'repositories']