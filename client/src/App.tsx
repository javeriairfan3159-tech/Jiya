import { useEffect, useMemo, useState } from "react";
import { api } from "./api";
import type { Task } from "./types";

export default function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    api
      .listTasks()
      .then(setTasks)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  const remaining = useMemo(() => tasks.filter((t) => !t.done).length, [tasks]);

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) return;
    setSubmitting(true);
    setError(null);
    try {
      const task = await api.createTask(trimmed);
      setTasks((prev) => [task, ...prev]);
      setTitle("");
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleToggle(task: Task) {
    try {
      const updated = await api.toggleTask(task.id, !task.done);
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
    } catch (e) {
      setError((e as Error).message);
    }
  }

  async function handleDelete(task: Task) {
    try {
      await api.deleteTask(task.id);
      setTasks((prev) => prev.filter((t) => t.id !== task.id));
    } catch (e) {
      setError((e as Error).message);
    }
  }

  return (
    <div className="app">
      <div className="card">
        <header className="header">
          <div className="brand">
            <span className="logo">J</span>
            <div>
              <h1>Jiya</h1>
              <p className="subtitle">A tiny full-stack task manager</p>
            </div>
          </div>
          <span className="counter" aria-label="tasks remaining">
            {remaining} left
          </span>
        </header>

        <form className="add-form" onSubmit={handleAdd}>
          <input
            className="input"
            placeholder="What needs doing?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            aria-label="New task title"
          />
          <button className="btn" type="submit" disabled={submitting || !title.trim()}>
            {submitting ? "Adding…" : "Add task"}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        {loading ? (
          <p className="muted">Loading tasks…</p>
        ) : tasks.length === 0 ? (
          <p className="muted">No tasks yet. Add one above to get started.</p>
        ) : (
          <ul className="list">
            {tasks.map((task) => (
              <li key={task.id} className={`item ${task.done ? "done" : ""}`}>
                <label className="item-main">
                  <input
                    type="checkbox"
                    checked={task.done}
                    onChange={() => handleToggle(task)}
                  />
                  <span className="item-title">{task.title}</span>
                </label>
                <button
                  className="delete"
                  onClick={() => handleDelete(task)}
                  aria-label={`Delete ${task.title}`}
                >
                  ✕
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
      <footer className="footer">
        Built with React, Vite &amp; Express · data served from the Jiya API
      </footer>
    </div>
  );
}
