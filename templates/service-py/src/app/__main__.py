"""Entry point: python -m app"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from app.config import Config
from app.health import health


class Handler(BaseHTTPRequestHandler):
    # do_GET: name is fixed by the BaseHTTPRequestHandler interface.
    def do_GET(self) -> None:
        if self.path == "/health":
            self._json(200, {"status": health().status, "uptimeSeconds": health().uptime_seconds})
            return
        self._json(404, {"error": "not found", "path": self.path})

    def _json(self, code: int, body: dict[str, object]) -> None:
        payload = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt: str, *args: object) -> None:
        print(json.dumps({"level": "info", "msg": fmt % args}))


def main() -> None:
    config = Config.from_env()
    print(json.dumps({"level": "info", "msg": "listening", "port": config.port}))
    HTTPServer(("", config.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
