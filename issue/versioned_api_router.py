from enum import Enum
from typing import Any, Callable, Optional, Sequence, Tuple

from fastapi import APIRouter, params
from fastapi.datastructures import Default
from fastapi.routing import APIRoute
from fastapi.types import DecoratedCallable
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import BaseRoute, Match
from starlette.types import ASGIApp, Receive, Scope, Send


class VersionedAPIRoute(APIRoute):
    @property
    def endpoint_version(self) -> str:
        return str(self.endpoint.__api_version__)  # type:ignore

    def is_version_matching(self, scope: Scope) -> bool:
        if "requested_version" not in scope or "latest_version" not in scope:
            raise HTTPException(
                500,
                f"Required keys are not present in scope. Are you using the AcceptHeaderVersionMiddleware???\nCurrent Scope is {scope}",
            )
        requested_version = scope["requested_version"]
        is_latest = self.endpoint_version == "latest"

        return bool(
            (is_latest and requested_version == scope["latest_version"])
            or self.endpoint_version == requested_version
        )

    def matches(self, scope: Scope) -> Tuple[Match, Scope]:
        match, child_scope = super().matches(scope)

        if match == Match.NONE or match == Match.PARTIAL:
            return match, child_scope
        if self.is_version_matching(scope):
            return Match.FULL, child_scope
        else:
            return Match.PARTIAL, child_scope

    async def handle(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not self.is_version_matching(scope):
            if "app" in scope:
                raise HTTPException(
                    406,
                    f"Requested version {scope['requested_version']} does not exist. "
                    f"Latest available version is {scope['latest_version']}.",
                )
            else:
                response = PlainTextResponse("Not Acceptable", status_code=406)
            await response(scope, receive, send)
        await super().handle(scope, receive, send)


class VersionedAPIRouter(APIRouter):
    def __init__(
        self,
        *,
        prefix: str = "",
        tags: Optional[list[str | Enum]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: type[Response] = Default(JSONResponse),
        responses: Optional[dict[int | str, dict[str, Any]]] = None,
        callbacks: Optional[list[BaseRoute]] = None,
        routes: Optional[list[BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: type[VersionedAPIRoute] = VersionedAPIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            default_response_class=default_response_class,
            responses=responses,
            callbacks=callbacks,
            routes=routes,
            redirect_slashes=redirect_slashes,
            default=default,
            dependency_overrides_provider=dependency_overrides_provider,
            route_class=route_class,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            deprecated=deprecated,
            include_in_schema=include_in_schema,
        )

    def version(
        self, api_version: str
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            func.__api_version__ = api_version  # type:ignore
            return func

        return decorator
