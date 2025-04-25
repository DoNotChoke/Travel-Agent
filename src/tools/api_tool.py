from typing import Optional, Dict, Any
import aiohttp
from aiohttp import ClientSession, ClientResponseError


class APIRequestError(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.status_code = status_code
        super().__init__(message)


class APIRequest:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session: Optional[ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.default_headers)
        return self

    async def __aexit__(self, *args):
        await self.session.close()

    @property
    def default_headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "User-Agent": "AI-Agent/1.0"
        }

    async def api_request(
            self,
            endpoint: str = "",
            method: str = "GET",
            params: Optional[Dict] = None,
            data: Optional[Dict] = None,
            headers: Optional[Dict] = None,
            timeout: int = 10
    ) -> Any:
        if not self.session:
            raise APIRequestError("Session not initialized. Use async with APIRequest()")

        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        headers = {**self.default_headers, **(headers or {})}

        try:
            async with self.session.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    json=data,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:

                response.raise_for_status()
                return await response.json()

        except ClientResponseError as e:
            raise APIRequestError(f"HTTP Error: {e.message}", status_code=e.status)
        except aiohttp.ClientConnectionError:
            raise APIRequestError("Connection error")
        except aiohttp.ServerTimeoutError:
            raise APIRequestError("Request timed out")
        except Exception as e:
            raise APIRequestError(f"Request failed: {str(e)}")