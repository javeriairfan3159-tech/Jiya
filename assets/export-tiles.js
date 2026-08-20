const fs = require("fs");
const src = fs.readFileSync("/workspace/assets/cow-patterns.svg", "utf8");

function extract(id, w, h, out) {
  const start = src.indexOf(`<pattern id="${id}"`);
  const end = src.indexOf("</pattern>", start);
  const block = src.slice(start, end);
  const innerStart = block.indexOf(">") + 1;
  const inner = block.slice(innerStart);
  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">${inner}
</svg>`;
  fs.writeFileSync(out, svg);
  console.log("wrote", out);
}

extract("cowInkOnPink", 240, 200, "/workspace/assets/cow-ink-on-pink.svg");
extract("cowClassic", 280, 220, "/workspace/assets/cow-classic.svg");
extract("cowStrawberry", 280, 220, "/workspace/assets/cow-strawberry.svg");
