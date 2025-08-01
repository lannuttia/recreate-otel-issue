import re
from logging import Logger, getLogger
from typing import Final

from starlette.types import ASGIApp, Receive, Scope, Send


class AcceptHeaderVersionMiddleware:
    """
    Use this middleware to parse the Accept Header if present and get an API version
    from the vendor tree. See https://www.rfc-editor.org/rfc/rfc6838#section-3.2

    If incoming http or websocket request contains an Accept header with the following
    value: `"accept/vnd.vendor_prefix.v42+json"`, the scope of the ASGI application
    will then contain an `api_version` of 42.

    If the http or websocket request does not contain an Accept header, or if the accept
    header value does not use a proper format, the scope of the ASGI application will
    then contain an `api_version` that defaults to the provided `latest_version`
    """

    def __init__(
        self,
        app: ASGIApp,
        vendor_prefix: str,
        latest_version: str,
        *,
        log: Logger = getLogger("accept-header-middleware"),
    ) -> None:
        log.debug(f"Initializing {type(self).__name__}")
        self.app = app
        self.latest_version = latest_version
        self.accept_regex = rf"^application/vnd\.{vendor_prefix}\.v([0-9]+)\+.*"
        self._log = log
        log.debug(f"Successfully initialized {type(self).__name__}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        _type: Final = scope["type"]
        self._log.debug(
            f"{type(self).__name__} has been invoked with request of type: {_type}"
        )
        self._log.debug(f"Received scope: {scope!r}")
        if _type in ("http", "websocket"):
            headers = dict(scope["headers"])
            scope["latest_version"] = self.latest_version  # type: ignore[typeddict-unknown-key]
            scope["requested_version"] = self.latest_version  # type: ignore[typeddict-unknown-key]

            if b"accept" in headers:
                accept_header = headers[b"accept"].decode("latin1")
                self._log.debug(f'Found "Accept" header with value: {accept_header}')
                match = re.search(self.accept_regex, accept_header)
                if match is not None:
                    self._log.debug(
                        f"Accept header provided matched regex: {self.accept_regex!r}"
                    )
                    api_version = match.group(1)
                    if api_version is not None:
                        scope["requested_version"] = api_version  # type: ignore[typeddict-unknown-key]
                        self._log.debug(
                            f"The requested API version for this request is {api_version}"
                        )

        self._log.debug(f"Sending scope: {scope!r}")
        await self.app(scope, receive, send)
