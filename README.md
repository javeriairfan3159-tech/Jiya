# Jiya

A tiny full-stack task manager used as the reference application for this repository's
development environment. It demonstrates a real end-to-end flow: a React client talks to
an Express API to create, complete, and delete tasks.

## Stack

- **client/** — React 18 + TypeScript + Vite (dev server on port `5173`)
- **server/** — Express + TypeScript REST API (port `3001`), in-memory task store
- npm workspaces monorepo

## Getting started

```bash
npm install        # install all workspace dependencies
npm run dev        # start API (3001) and client (5173) together
```

Then open http://localhost:5173. The Vite dev server proxies `/api/*` to the Express
backend, so everything is served from a single origin during development.

## Useful commands

| Command | Description |
| --- | --- |
| `npm run dev` | Run the API and client dev servers concurrently |
| `npm run dev:server` | Run only the Express API (`tsx watch`) |
| `npm run dev:client` | Run only the Vite client |
| `npm run build` | Type-check and build both workspaces |
| `npm run typecheck` | Type-check both workspaces without emitting |

## API

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/tasks` | List tasks |
| `POST` | `/api/tasks` | Create a task (`{ "title": string }`) |
| `PATCH` | `/api/tasks/:id` | Update `done`/`title` |
| `DELETE` | `/api/tasks/:id` | Delete a task |
