import assert from "node:assert/strict";
import { test } from "node:test";

import { health } from "./health.ts";
import { _internal } from "./config.ts";

test("reports ok with a whole number of seconds of uptime", () => {
  const result = health(() => 12.7);
  assert.equal(result.status, "ok");
  assert.equal(result.uptimeSeconds, 12);
});

test("rejects a port that is not a valid TCP port", () => {
  assert.throws(() => _internal.port("70000"), /between 1 and 65535/);
  assert.throws(() => _internal.port("not-a-number"), /between 1 and 65535/);
});

test("rejects a missing required variable by name", () => {
  delete process.env.ABSENT_FOR_TEST;
  assert.throws(() => _internal.required("ABSENT_FOR_TEST"), /ABSENT_FOR_TEST/);
});
