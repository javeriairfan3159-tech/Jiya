#!/usr/bin/env node
/**
 * Generates an organic strawberry-cow SVG pattern (cream hide + pink/ink spots).
 */
const fs = require("fs");
const path = require("path");

function mulberry32(a) {
  return function () {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function blobPath(rng, cx, cy, rx, ry) {
  const points = 7 + Math.floor(rng() * 4);
  const coords = [];
  for (let i = 0; i < points; i++) {
    const a = (Math.PI * 2 * i) / points + (rng() - 0.5) * 0.35;
    const jr = 0.72 + rng() * 0.45;
    const x = cx + Math.cos(a) * rx * jr;
    const y = cy + Math.sin(a) * ry * jr;
    coords.push([x, y]);
  }
  let d = `M ${coords[0][0].toFixed(1)} ${coords[0][1].toFixed(1)} `;
  for (let i = 0; i < coords.length; i++) {
    const p0 = coords[i];
    const p1 = coords[(i + 1) % coords.length];
    const mx = (p0[0] + p1[0]) / 2;
    const my = (p0[1] + p1[1]) / 2;
    d += `Q ${p0[0].toFixed(1)} ${p0[1].toFixed(1)} ${mx.toFixed(1)} ${my.toFixed(1)} `;
  }
  d += "Z";
  return d;
}

function makePattern({ id, seed, width, height, fill, spots }) {
  const rng = mulberry32(seed);
  const paths = [];
  for (const spot of spots) {
    const count = spot.count;
    for (let i = 0; i < count; i++) {
      const cx = rng() * width;
      const cy = rng() * height;
      const rx = spot.minR + rng() * (spot.maxR - spot.minR);
      const ry = rx * (0.65 + rng() * 0.55);
      const rot = rng() * 360;
      const d = blobPath(rng, 0, 0, rx, ry);
      const opacity = spot.opacityMin + rng() * (spot.opacityMax - spot.opacityMin);
      paths.push(
        `<g transform="translate(${cx.toFixed(1)} ${cy.toFixed(1)}) rotate(${rot.toFixed(1)})">` +
          `<path d="${d}" fill="${spot.color}" fill-opacity="${opacity.toFixed(2)}"/></g>`
      );
    }
  }
  return `
  <pattern id="${id}" patternUnits="userSpaceOnUse" width="${width}" height="${height}">
    <rect width="${width}" height="${height}" fill="${fill}"/>
    ${paths.join("\n    ")}
  </pattern>`;
}

const classic = makePattern({
  id: "cowClassic",
  seed: 42,
  width: 280,
  height: 220,
  fill: "#FFFDF8",
  spots: [
    { count: 11, minR: 18, maxR: 42, color: "#141414", opacityMin: 0.92, opacityMax: 1 },
    { count: 9, minR: 8, maxR: 16, color: "#1A1A1A", opacityMin: 0.88, opacityMax: 1 },
    { count: 6, minR: 4, maxR: 8, color: "#111", opacityMin: 0.8, opacityMax: 1 },
  ],
});

const strawberry = makePattern({
  id: "cowStrawberry",
  seed: 77,
  width: 280,
  height: 220,
  fill: "#F8D5DE",
  spots: [
    { count: 10, minR: 16, maxR: 38, color: "#C2185B", opacityMin: 0.85, opacityMax: 1 },
    { count: 7, minR: 10, maxR: 22, color: "#1A1214", opacityMin: 0.78, opacityMax: 0.95 },
    { count: 8, minR: 5, maxR: 12, color: "#E23D86", opacityMin: 0.7, opacityMax: 0.95 },
  ],
});

const inkOnPink = makePattern({
  id: "cowInkOnPink",
  seed: 19,
  width: 240,
  height: 200,
  fill: "#F4A7C0",
  spots: [
    { count: 12, minR: 14, maxR: 36, color: "#171417", opacityMin: 0.9, opacityMax: 1 },
    { count: 8, minR: 6, maxR: 14, color: "#2A1A22", opacityMin: 0.85, opacityMax: 1 },
  ],
});

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0">
  <defs>
    ${classic}
    ${strawberry}
    ${inkOnPink}
  </defs>
</svg>
`;

fs.writeFileSync(path.join(__dirname, "cow-patterns.svg"), svg);
console.log("Wrote cow-patterns.svg");
