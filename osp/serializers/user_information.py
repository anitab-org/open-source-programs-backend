from rest_framework import serializers

from osp.models import UserInformation
from osp.serializers.user import UserSerializer


class UserInformationSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = UserInformation
        fields = ["id", "name", "user", "user_type", "zulip_id", "github_username"]
