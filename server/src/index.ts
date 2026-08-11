import cors from "cors";
import express, { type Request, type Response } from "express";
import { randomUUID } from "node:crypto";

interface Task {
  id: string;
  title: string;
  done: boolean;
  createdAt: string;
}

const PORT = Number(process.env.PORT ?? 3001);

const app = express();
app.use(cors());
app.use(express.json());

// In-memory store seeded with a couple of example tasks. This keeps the
// reference app dependency-free while still exercising a real request flow.
const tasks: Task[] = [
  {
    id: randomUUID(),
    title: "Welcome to Jiya — add your first task",
    done: false,
    createdAt: new Date().toISOString(),
  },
];

app.get("/api/health", (_req: Request, res: Response) => {
  res.json({ status: "ok", uptime: process.uptime() });
});

app.get("/api/tasks", (_req: Request, res: Response) => {
  res.json(tasks);
});

app.post("/api/tasks", (req: Request, res: Response) => {
  const title = typeof req.body?.title === "string" ? req.body.title.trim() : "";
  if (!title) {
    return res.status(400).json({ error: "title is required" });
  }
  const task: Task = {
    id: randomUUID(),
    title,
    done: false,
    createdAt: new Date().toISOString(),
  };
  tasks.unshift(task);
  res.status(201).json(task);
});

app.patch("/api/tasks/:id", (req: Request, res: Response) => {
  const task = tasks.find((t) => t.id === req.params.id);
  if (!task) {
    return res.status(404).json({ error: "task not found" });
  }
  if (typeof req.body?.done === "boolean") {
    task.done = req.body.done;
  }
  if (typeof req.body?.title === "string" && req.body.title.trim()) {
    task.title = req.body.title.trim();
  }
  res.json(task);
});

app.delete("/api/tasks/:id", (req: Request, res: Response) => {
  const index = tasks.findIndex((t) => t.id === req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: "task not found" });
  }
  const [removed] = tasks.splice(index, 1);
  res.json(removed);
});

app.listen(PORT, () => {
  console.log(`[jiya] API server listening on http://localhost:${PORT}`);
});
