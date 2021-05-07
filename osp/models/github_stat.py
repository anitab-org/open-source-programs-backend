from django.db import models

from osp.models import AbstractTimestamp
from osp.models.user_information import UserInformation


class GithubStat(AbstractTimestamp):
    user_information = models.OneToOneField(UserInformation, on_delete=models.CASCADE)
    total_prs_open = models.IntegerField(default=0)
    total_prs_closed = models.IntegerField(default=0)
    total_prs_merged = models.IntegerField(default=0)
    total_issues_created = models.IntegerField(default=0)
    total_comments_on_issues = models.IntegerField(default=0)
    total_prs_reviewed = models.IntegerField(default=0)
