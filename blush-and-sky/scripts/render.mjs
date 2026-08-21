#!/usr/bin/env node
import { spawn } from "child_process";
import http from "http";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "exports");
fs.mkdirSync(OUT, { recursive: true });

const jobs = [
  { file: "designs/invite-5x7.html", out: "invite-5x7.png", w: 1500, h: 2100 },
  { file: "designs/invite-mobile.html", out: "invite-mobile.png", w: 1080, h: 1920 },
  { file: "designs/details-card.html", out: "details-card.png", w: 1500, h: 2100 },
  { file: "designs/welcome-sign.html", out: "welcome-sign.png", w: 1800, h: 2400 },
  { file: "designs/favor-tag.html", out: "favor-tag.png", w: 1200, h: 1200 },
  { file: "designs/books-for-baby.html", out: "books-for-baby.png", w: 1500, h: 1500 },
  { file: "designs/diaper-raffle.html", out: "diaper-raffle.png", w: 1500, h: 900 },
];

function mime(p) {
  if (p.endsWith(".html")) return "text/html; charset=utf-8";
  if (p.endsWith(".svg")) return "image/svg+xml";
  if (p.endsWith(".css")) return "text/css";
  if (p.endsWith(".js")) return "text/javascript";
  if (p.endsWith(".png")) return "image/png";
  if (p.endsWith(".ttf")) return "font/ttf";
  return "application/octet-stream";
}

const server = http.createServer((req, res) => {
  const urlPath = decodeURIComponent(req.url.split("?")[0]);
  const filePath = path.join(ROOT, urlPath);
  if (!filePath.startsWith(ROOT)) {
    res.writeHead(403);
    res.end();
    return;
  }
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end("not found");
      return;
    }
    res.writeHead(200, { "Content-Type": mime(filePath) });
    res.end(data);
  });
});

function chromeShot(job, port) {
  return new Promise((resolve, reject) => {
    const outPath = path.join(OUT, job.out);
    const userDir = fs.mkdtempSync(path.join("/tmp", "chrome-render-"));
    const args = [
      "--headless=new",
      "--disable-gpu",
      "--hide-scrollbars",
      "--no-sandbox",
      "--disable-extensions",
      "--disable-background-networking",
      "--disable-sync",
      "--disable-default-apps",
      "--no-first-run",
      "--mute-audio",
      "--metrics-recording-only",
      `--user-data-dir=${userDir}`,
      "--force-device-scale-factor=2",
      `--window-size=${job.w},${job.h}`,
      `--screenshot=${outPath}`,
      "--virtual-time-budget=12000",
      "--run-all-compositor-stages-before-draw",
      `http://127.0.0.1:${port}/${job.file}`,
    ];
    const child = spawn("timeout", ["40", "google-chrome", ...args], { stdio: "inherit" });
    child.on("exit", (code) => {
      fs.rmSync(userDir, { recursive: true, force: true });
      if (code === 0 || code === 124) {
        if (!fs.existsSync(outPath)) reject(new Error(`no screenshot for ${job.file}`));
        else resolve(outPath);
      } else {
        reject(new Error(`chrome exited ${code} for ${job.file}`));
      }
    });
  });
}

server.listen(0, "127.0.0.1", async () => {
  const port = server.address().port;
  console.log("serving on", port);
  try {
    for (const job of jobs) {
      console.log("rendering", job.file);
      const out = await chromeShot(job, port);
      const stat = fs.statSync(out);
      console.log("wrote", out, stat.size);
    }
  } catch (err) {
    console.error(err);
    process.exitCode = 1;
  } finally {
    server.close();
  }
});
