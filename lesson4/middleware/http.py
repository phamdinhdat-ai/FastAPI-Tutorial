import time 
import sys 

from pathlib import Path

from starlette.responses import Response 
sys.path.append(str(Path(__file__).parent.parent))
from typing import List, Optional, Any, Callable
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from utils.logger import LoggingConfig, Logger

LOGGER = Logger(__file__, log_file='http.log')

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        response_time = time.time()
        process_time = time.time() - start_time
        
        LOGGER.log.info(
            f"{request.client.host} - \"{request.method} {request.url.path } {request.scope['http_version']}\" {request.status_code} { process_time:.2f}s"
        )
        return Response
    