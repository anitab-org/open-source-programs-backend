from os import getenv

from dotenv import load_dotenv
from github import Github
from github.GithubException import GithubException

load_dotenv()

GITHUB_API_KEY = getenv("GITHUB_API_KEY", None)
ORGANIZATION = "anitab-org"


class GithubClient:
    def __init__(self):
        self._client = Github(GITHUB_API_KEY) if GITHUB_API_KEY else Github()

    def find_stats(self, username):
        if username is None:
            return None
        # NOTE: 5 requests in total
        try:
            non_merged_prs = self._find_prs(username, "unmerged")
            merged_prs = self._find_prs(username, "merged")
            issues_no = self._find_num_of_issues(username)
            comments_no = self._find_num_of_comments(username)
            pr_reviews_no = self._find_num_of_pr_reviews(username)
            return {
                "total_prs_open": non_merged_prs["open"],
                "total_prs_closed": non_merged_prs["closed"],
                "total_prs_merged": merged_prs["closed"],
                "total_issues_created": issues_no,
                "total_comments_on_issues": comments_no,
                "total_prs_reviewed": pr_reviews_no,
            }
        except GithubException as e:
            message = "Fetching details from Github failed! Try again later."
            error_list = e.data.get("errors", [])
            if len(error_list) > 0:
                message = error_list[0].get("message", message)
            return {"message": message, "status": e.status}

        except Exception:
            return {"message": "An unexpected error occurred. Please, try again later!", "status": 500}

    # NOTE: all of the methods count issues/PRs created both in archived and active repos
    # to filter them, add archived:true/false to the query
    # private API
    def _find_num_of_issues(self, username):
        issue_list = self._client.search_issues(f"author:{username} type:issue org:{ORGANIZATION}")
        return issue_list.totalCount

    def _find_prs(self, username, merge_status="merged"):
        if merge_status not in ("merged", "unmerged"):
            raise ValueError("PR merge status can be: merged on unmerged.")
        pr_list = self._client.search_issues(f"author:{username} type:pr is:{merge_status} org:{ORGANIZATION}")
        if merge_status == "merged":
            prs = {"closed": 0}
        else:
            prs = {"open": 0, "closed": 0}
        for pr in pr_list:
            try:
                prs[pr.state] += 1
            except KeyError:
                continue
        return prs

    def _find_num_of_pr_reviews(self, username):
        reviews = self._client.search_issues(f"type:pr reviewed-by:{username} org:{ORGANIZATION}")
        return reviews.totalCount

    def _find_num_of_comments(self, username):
        num_of_comments = self._client.search_issues(f"commenter:{username} org:{ORGANIZATION}")
        return num_of_comments.totalCount


"""
NOTE:
The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret,
you can make up to 30 requests per minute. For unauthenticated requests, the rate limit allows you to make up to
10 requests per minute.
https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
For unauthenticated requests, the rate limit allows for up to 60 requests per hour.
Unauthenticated requests are associated with the originating IP address, and not the user making requests.
https://docs.github.com/en/rest/reference/search
"""
