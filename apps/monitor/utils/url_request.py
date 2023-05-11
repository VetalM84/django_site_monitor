"""Class to work with requests to urls via httpx lib."""

from random import randint

from httpx import AsyncClient, Response

from apps.monitor.models import ProjectModule


class URLRequest:
    """URL request class."""

    def __init__(self):
        """Init."""
        # TODO: add headers to AsyncClient
        # TODO: add timeout to AsyncClient
        self._headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"}
        self.client = AsyncClient(follow_redirects=True, headers=self._headers)

    async def get_url(self, url: str) -> Response:
        """Request url with GET method."""
        try:
            async with self.client:
                response = await self.client.get(url=url)
                return response
        except Exception as e:
            print(e)
            return Response(status_code=500)

    async def post_url(self, url: str, data: dict) -> Response:
        """Request url with POST method."""
        try:
            async with self.client:
                response = await self.client.post(url=url, data=data)
                return response
        except Exception as e:
            print(e)
            return Response(status_code=500)

    async def get_url_with_pagination(self, module: ProjectModule) -> Response:
        """Send GET request to url with pagination."""
        url = module.url
        # use random page number if pagination is enabled
        if module.pagination:
            url = module.url.replace("$page$", str(randint(1, module.pagination)))

        response = await self.get_url(url=url)
        return response
