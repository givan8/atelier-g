/**
 * Configuration comes from the environment and is validated once, at startup.
 *
 * House rule 6: fail loudly. A missing or malformed variable stops the process
 * here rather than producing a confusing failure later.
 */

function required(name: string): string {
  const value = process.env[name];
  if (value === undefined || value === "") {
    throw new Error(`missing required environment variable: ${name}`);
  }
  return value;
}

function port(raw: string): number {
  const n = Number(raw);
  if (!Number.isInteger(n) || n < 1 || n > 65535) {
    throw new Error(`PORT must be an integer between 1 and 65535, got ${raw}`);
  }
  return n;
}

export const config = {
  port: port(process.env.PORT ?? "8080"),
  logLevel: process.env.LOG_LEVEL ?? "info",
} as const;

export const _internal = { required, port };
