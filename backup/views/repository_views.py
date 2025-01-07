from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
#from django.shortcuts import get_object_or_404
from ..models.user import User
from ..models.repository import Repository
from ..serializers.repository import RepositorySerializer
from ..github_utils import validate_github_repo, validate_username_and_repo_url

class RepositoryViewSet(viewsets.ViewSet):
    queryset = Repository.objects.all()
    serializer_class = RepositorySerializer
    http_method_names = ['get', 'post', 'delete']


    def create(self, request, *args, **kwargs):
        return Response({"error": "Endpoint disabled."}, status=status.HTTP_401_UNAUTHORIZED) 


    @action(detail=False, methods=['post'], url_path='backup_repo')
    def backup_repository(self, request):
        username = request.data.get("username")
        repo_url = request.data.get("github_url")            
        is_valid, message = validate_username_and_repo_url(username, repo_url)
        if not is_valid:
            return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": f"User '{username}' not found in the database."},
                status=status.HTTP_404_NOT_FOUND)
            
        # repo_name = repo_url.split("/")[-1] 
        repo_name = message
        response = validate_github_repo(username, repo_name)
        if response.status_code != 200:
            return Response(
                {"error": f"Repository '{repo_name}' does not exist or does not belong to the user '{username}'."},
                status=status.HTTP_404_NOT_FOUND
            )

        repository, created = Repository.objects.get_or_create(
            owner=user,
            github_url=repo_url,
            defaults={"name": repo_name}
        )

        if not created:
            return Response(
                {"error": "Repository is already backed up in the database."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(repository)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    @action(detail=False, methods=['delete'], url_path="delete_by_url")
    def delete_by_url(self, request):
        repo_url = request.data.get("github_url")
        if not repo_url:
            return Response({"error": "The 'github_url' repository URL is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            repository = Repository.objects.get(github_url=repo_url)
            repository.delete()
            return Response({"message": f"Repository '{repo_url}' deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Repository.DoesNotExist:
            return Response({"error": "Repository does not exist in the database."}, status=status.HTTP_404_NOT_FOUND)
