from django.forms import ValidationError
from rest_framework import viewsets, permissions
from .models import Project, Environment, Secret
from .serializers import ProjectSerializer, EnvironmentSerializer, SecretSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EnvironmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnvironmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        qs = Environment.objects.all()
        if project_id:
            qs = qs.filter(project_id=project_id)
        return qs

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        if not project_id:
            raise ValidationError("Project ID is required.")
        
        try:
            project = Project.objects.get(id=project_id, user=self.request.user)
        except Project.DoesNotExist:
            raise ValidationError("You do not own this project.")

        serializer.save()



class SecretViewSet(viewsets.ModelViewSet):
    serializer_class = SecretSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Secret.objects.filter(user=self.request.user)
        project_id = self.request.query_params.get('project')
        environment_id = self.request.query_params.get('environment')
        if project_id:
            qs = qs.filter(project_id=project_id)
        if environment_id:
            qs = qs.filter(environment_id=environment_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        instance = self.get_queryset().get(id=response.data['id'])
        response.data['decrypted_value'] = instance.get_decrypted_value()
        return response

