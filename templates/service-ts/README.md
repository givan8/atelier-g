# {{PROJECT_NAME}}

<!-- One sentence: what this does and who it is for. Replace the TODOs below with
     what is actually true. A README that says TODO on day one says TODO forever. -->

TODO — what this service does.

Built from the `{{TEMPLATE}}` template of
[atelier-g](https://github.com/givan8/atelier-g). Agents working here should read
[`AGENTS.md`](AGENTS.md) first.

## Run locally

```bash
npm install          # first run: commit the package-lock.json this produces
cp .env.example .env
npm run dev
curl localhost:8080/health
```

CI uses `npm ci`, which requires that lock file. Commit it with the scaffold
commit or CI will fail on the first push.

## Test

```bash
npm test           # once
npm run test:watch # while working
npm run check      # types + lint + tests, the same as CI
```

## Layout

```
src/            application code
src/index.ts    entry point
docs/adr/       decisions — read these before changing the design
```

## Configuration

All configuration comes from the environment. [`.env.example`](.env.example) lists
every variable the service reads. No secrets in the repository, ever.

## Deploy

TODO — how this is deployed, and how to roll it back.
