from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from osp.models import UserInformation
from osp.models.github_stat import GithubStat
from osp.serializers.github_stat import GithubStatSerializer
from osp.utils.github_api_client import GithubClient


class GithubStatView(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = GithubStatSerializer
    github_client = GithubClient()
    queryset = GithubStat.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id", None)
        if user_id is None:
            user = self.request.user
            user_id = user.id
        return self.queryset.filter(user_information__user_id=user_id)

    def create(self, request):
        user = self.request.user
        try:
            user_information = UserInformation.objects.get(user__id=user.id)
        except UserInformation.DoesNotExist:
            return Response(
                {
                    "message": "User information does not exist. You must create it in order to fetch the GitHub "
                    "details!"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            github_stat = GithubStat.objects.get(user_information__user_id=user.id)
        except GithubStat.DoesNotExist:
            github_stat = None
        github_stat_data = self.github_client.find_stats(user_information.github_username)
        if "message" in github_stat_data:
            return Response({"message": github_stat_data["message"]}, status=github_stat_data["status"])
        if github_stat_data is None:
            return Response(
                {"message": "An error occurred. Check the Github username you provided."},
                status=status.HTTP_404_NOT_FOUND,
            )
        if github_stat is None:
            serializer = self.serializer_class(data=github_stat_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_information_id=user_information.id)

        else:
            serializer = self.serializer_class(github_stat, data=github_stat_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
