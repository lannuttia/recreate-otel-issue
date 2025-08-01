Without opentelemetry-instrument everything works as expected:

```shell
$ python -m uvicorn issue.start:app
$ curl http://127.0.0.1:8000/
```

With opentelemetry-instrument the request fails because the AcceptHeaderVersionMiddleware is not ran as it should be:

```shell
$ podman-compose up
$ source .env
$ opentelemetry-instrument python -m uvicorn issue.start:app
$ curl http://127.0.0.1:8000/
```

```

Output of `opentelemetry-bootstrap`:

```plaintext
opentelemetry-instrumentation-asyncio==0.56b0
opentelemetry-instrumentation-dbapi==0.56b0
opentelemetry-instrumentation-logging==0.56b0
opentelemetry-instrumentation-sqlite3==0.56b0
opentelemetry-instrumentation-threading==0.56b0
opentelemetry-instrumentation-urllib==0.56b0
opentelemetry-instrumentation-wsgi==0.56b0
opentelemetry-instrumentation-asgi==0.56b0
opentelemetry-instrumentation-click==0.56b0
opentelemetry-instrumentation-fastapi==0.56b0
opentelemetry-instrumentation-grpc==0.56b0
opentelemetry-instrumentation-requests==0.56b0
opentelemetry-instrumentation-starlette==0.56b0
opentelemetry-instrumentation-system-metrics==0.56b0
opentelemetry-instrumentation-tortoiseorm==0.56b0
opentelemetry-instrumentation-urllib3==0.56b0
```

Output of `pip freeze`:

```plaintext
annotated-types==0.7.0
anyio==4.9.0
asgiref==3.9.1
certifi==2025.7.14
charset-normalizer==3.4.2
click==8.2.1
fastapi==0.116.1
googleapis-common-protos==1.70.0
grpcio==1.74.0
h11==0.16.0
idna==3.10
importlib_metadata==8.7.0
opentelemetry-api==1.35.0
opentelemetry-exporter-otlp-proto-common==1.35.0
opentelemetry-exporter-otlp-proto-grpc==1.35.0
opentelemetry-exporter-otlp-proto-http==1.35.0
opentelemetry-instrumentation==0.56b0
opentelemetry-instrumentation-asgi==0.56b0
opentelemetry-instrumentation-asyncio==0.56b0
opentelemetry-instrumentation-click==0.56b0
opentelemetry-instrumentation-dbapi==0.56b0
opentelemetry-instrumentation-fastapi==0.56b0
opentelemetry-instrumentation-grpc==0.56b0
opentelemetry-instrumentation-logging==0.56b0
opentelemetry-instrumentation-requests==0.56b0
opentelemetry-instrumentation-sqlite3==0.56b0
opentelemetry-instrumentation-starlette==0.56b0
opentelemetry-instrumentation-system-metrics==0.56b0
opentelemetry-instrumentation-threading==0.56b0
opentelemetry-instrumentation-tortoiseorm==0.56b0
opentelemetry-instrumentation-urllib==0.56b0
opentelemetry-instrumentation-urllib3==0.56b0
opentelemetry-instrumentation-wsgi==0.56b0
opentelemetry-propagator-b3==1.35.0
opentelemetry-proto==1.35.0
opentelemetry-sdk==1.35.0
opentelemetry-semantic-conventions==0.56b0
opentelemetry-util-http==0.56b0
packaging==25.0
protobuf==6.31.1
psutil==7.0.0
pydantic==2.11.7
pydantic_core==2.33.2
# Editable Git install with no remote (recreate-otel-issue==0.1.0)
-e /home/alannutt/Projects/lannuttia/recreate-otel-issue
requests==2.32.4
sniffio==1.3.1
splunk-opentelemetry==2.6.0
starlette==0.47.2
typing-inspection==0.4.1
typing_extensions==4.14.1
urllib3==2.5.0
uvicorn==0.35.0
wrapt==1.17.2
zipp==3.23.0
```

Output of `cat /etc/os-release`:
```plaintext
NAME="Fedora Linux"
VERSION="42 (Workstation Edition)"
RELEASE_TYPE=stable
ID=fedora
VERSION_ID=42
VERSION_CODENAME=""
PLATFORM_ID="platform:f42"
PRETTY_NAME="Fedora Linux 42 (Workstation Edition)"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:fedoraproject:fedora:42"
DEFAULT_HOSTNAME="fedora"
HOME_URL="https://fedoraproject.org/"
DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora/f42/"
SUPPORT_URL="https://ask.fedoraproject.org/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=42
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=42
SUPPORT_END=2026-05-13
VARIANT="Workstation Edition"
VARIANT_ID=workstation
```
