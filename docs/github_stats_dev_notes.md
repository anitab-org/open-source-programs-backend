# GitHub API Limits:

1. [The Search API](https://docs.github.com/en/rest/reference/search) has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret, you can make up to 30 requests per minute. For unauthenticated requests, the rate limit allows you to make up to
10 requests per minute ([original GitHub docs resource](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)).
2. For unauthenticated requests, the rate limit allows for up to 60 requests per hour. Unauthenticated requests are associated with the originating IP address, and not the user making requests.
