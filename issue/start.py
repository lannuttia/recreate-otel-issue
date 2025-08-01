from fastapi import FastAPI

from issue.accept_header_version_middleware import AcceptHeaderVersionMiddleware
from issue.versioned_api_router import VersionedAPIRouter

app = FastAPI()
app.add_middleware(
    AcceptHeaderVersionMiddleware, vendor_prefix="vendor", latest_version="1"
)

router = VersionedAPIRouter()


@router.get("/")
@router.version("1")
def _():
    return None


app.include_router(router)
