# from rest_framework import serializers
# from .models import Project, Environment, Secret

# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = ['id', 'name', 'user']
#         read_only_fields = ['user']

# class EnvironmentSerializer(serializers.ModelSerializer):
#     class Meta: 
#         model = Environment
#         fields = ['id', 'name', 'project']

# class SecretSerializer(serializers.ModelSerializer):
#     decrypted_value = serializers.SerializerMethodField()

#     class Meta:
#         model = Secret
#         fields = ['id', 'key', 'decrypted_value', 'version', 'environment', 'project', 'created_at', 'user']
#         read_only_fields = ['decrypted_value', 'created_at', 'user']

#     def get_decrypted_value(self, obj):
#         return obj.get_decrypted_value()

from rest_framework import serializers
from .models import Project, Environment, Secret

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'user']
        read_only_fields = ['user']

class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Environment
        fields = ['id', 'name', 'project']

class SecretSerializer(serializers.ModelSerializer):
    decrypted_value = serializers.SerializerMethodField()

    class Meta:
        model = Secret
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'decrypted_value']

    def get_decrypted_value(self, obj):
        return obj.get_decrypted_value()
