import { createServer } from "node:http";

import { config } from "./config.ts";
import { health } from "./health.ts";

const server = createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify(health()));
    return;
  }

  res.writeHead(404, { "content-type": "application/json" });
  res.end(JSON.stringify({ error: "not found", path: req.url }));
});

server.listen(config.port, () => {
  console.log(JSON.stringify({ level: "info", msg: "listening", port: config.port }));
});
