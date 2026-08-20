const fs = require("fs");
const path = require("path");

const W = 1360;
const H = 1960;
const R = 28;
const BAND = 10;

function scallopPath(w, h, r, band) {
  const x0 = band;
  const y0 = band;
  const x1 = w - band;
  const y1 = h - band;
  const nTop = Math.round((x1 - x0) / (2 * r));
  const nSide = Math.round((y1 - y0) / (2 * r));
  const sx = (x1 - x0) / nTop;
  const sy = (y1 - y0) / nSide;

  let d = `M ${x0} ${y0}`;
  for (let i = 0; i < nTop; i++) {
    d += ` A ${r} ${r} 0 0 1 ${(x0 + (i + 1) * sx).toFixed(2)} ${y0}`;
  }
  for (let i = 0; i < nSide; i++) {
    d += ` A ${r} ${r} 0 0 1 ${x1} ${(y0 + (i + 1) * sy).toFixed(2)}`;
  }
  for (let i = 0; i < nTop; i++) {
    d += ` A ${r} ${r} 0 0 1 ${(x1 - (i + 1) * sx).toFixed(2)} ${y1}`;
  }
  for (let i = 0; i < nSide; i++) {
    d += ` A ${r} ${r} 0 0 1 ${x0} ${(y1 - (i + 1) * sy).toFixed(2)}`;
  }
  d += " Z";
  return d;
}

const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="#f4a8c0"/>
  <path d="${scallopPath(W, H, R, BAND)}" fill="#fbf6ee"/>
</svg>
`;

fs.writeFileSync(path.join(__dirname, "scallop-frame.svg"), svg);
console.log("wrote scallop-frame.svg", W, H, R);
