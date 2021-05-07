from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from osp.models import UserInformation
from osp.serializers.github_stat import GithubStatSerializer
from osp.serializers.user_information import UserInformationSerializer
from osp.utils.github_api_client import GithubClient
from osp.utils.zulip_api import get_zulip_user


class UserInformationView(viewsets.ModelViewSet):

    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = UserInformationSerializer
    github_serializer_class = GithubStatSerializer
    queryset = UserInformation.objects.all()
    github_client = GithubClient()

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id", None)
        user = self.request.user
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user_id=user.id)
        return queryset

    def create(self, request):
        user = self.request.user
        serializer = UserInformationSerializer(data=request.data)
        if UserInformation.objects.filter(user_id=user.id).exists():
            return Response("Information already filled", status=status.HTTP_409_CONFLICT)
        response = get_zulip_user(request.data["zulip_id"])
        github_stat_data = self.github_client.find_stats(request.data.get("github_username"))
        if "message" in github_stat_data:
            return Response({"message": github_stat_data["message"]}, status=github_stat_data["status"])
        if response and github_stat_data:
            serializer.is_valid(raise_exception=True)
            user_information = serializer.save(user_id=user.id)
            # create GitHub stats
            github_serializer = self.github_serializer_class(data=github_stat_data)
            github_serializer.is_valid(raise_exception=True)
            github_serializer.save(user_information=user_information)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("No user found with the Zulip ID entered.", status=status.HTTP_404_NOT_FOUND)
