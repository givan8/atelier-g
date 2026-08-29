export type Health = {
  status: "ok";
  uptimeSeconds: number;
};

export function health(now: () => number = process.uptime): Health {
  return { status: "ok", uptimeSeconds: Math.floor(now()) };
}
