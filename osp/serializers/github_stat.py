from rest_framework import serializers

from osp.models import GithubStat


class GithubStatSerializer(serializers.ModelSerializer):
    github_username = serializers.CharField(source="user_information.github_username", read_only=True)

    class Meta:
        model = GithubStat
        fields = [
            "id",
            "github_username",
            "total_prs_open",
            "total_prs_closed",
            "total_prs_merged",
            "total_issues_created",
            "total_comments_on_issues",
            "total_prs_reviewed",
            "updated_on",
        ]
