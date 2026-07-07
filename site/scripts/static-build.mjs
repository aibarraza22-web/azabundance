import { mkdirSync, copyFileSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';

const pages = [
  ['dist/index.html', 'Arizona Abundance Index', 'Is Arizona actually building?', 'A quarterly, methodology-transparent scoreboard for Arizona housing, energy, chips, data centers, and permitting capacity.'],
  ['dist/index/index.html', 'Scoreboard | Arizona Abundance Index', 'Scoreboard scaffold', 'This Phase 0 page uses dummy data only. Real metrics will not be charted until source files are fetched, snapshotted, parsed, and validated.'],
  ['dist/methodology/index.html', 'Methodology | Arizona Abundance Index', 'Methodology', 'Every published number must trace to snapshotted raw data, a validated tidy row, and a documented vintage.'],
  ['dist/data/index.html', 'Data | Arizona Abundance Index', 'Data downloads', 'Static CSV and JSON outputs will be published here after validation.'],
  ['dist/essays/index.html', 'Essays | Arizona Abundance Index', 'Essays', 'Essays may argue, but every number in them must come from the pipeline.'],
  ['dist/about/index.html', 'About | Arizona Abundance Index', 'About', 'The Arizona Abundance Index is a data journalism project focused on reproducible public-interest infrastructure metrics.'],
];

function shell(title, h1, body) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title><style>:root{color:#17202a;background:#fbfaf7;font-family:Inter,ui-sans-serif,system-ui,sans-serif;--accent:#9a3412}body{margin:0}header,main,footer{max-width:1080px;margin:0 auto;padding:1.25rem}header{border-bottom:1px solid #e5e1d8;display:flex;justify-content:space-between;gap:1rem;align-items:center}nav{display:flex;flex-wrap:wrap;gap:.75rem}a{color:var(--accent)}.brand{color:#17202a;font-weight:800;text-decoration:none}h1{font-size:clamp(2.2rem,5vw,4.75rem);line-height:.95;max-width:900px;letter-spacing:-.05em}.lede{font-size:1.25rem;line-height:1.6;max-width:760px}.card{background:white;border:1px solid #e5e1d8;border-radius:16px;padding:1.25rem}</style></head><body><header><a class="brand" href="/">Arizona Abundance Index</a><nav><a href="/index/">Index</a><a href="/methodology/">Methodology</a><a href="/data/">Data</a><a href="/essays/">Essays</a><a href="/about/">About</a></nav></header><main><h1>${h1}</h1><p class="lede">${body}</p>${title.startsWith('Scoreboard') ? '<section class="card"><h2>Phase 0 placeholder metric</h2><p>Dummy chart: 100 → 112 → 108 → 121</p><p><a href="/data/placeholder_metric.json">Download placeholder JSON</a> · <a href="/methodology/">Methodology</a></p></section>' : ''}</main><footer>Built for reproducible, methodology-transparent data journalism.</footer></body></html>`;
}

rmSync('dist', { recursive: true, force: true });
for (const [path, title, h1, body] of pages) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, shell(title, h1, body));
}
if (existsSync('public/data/placeholder_metric.json')) {
  mkdirSync(join('dist', 'data'), { recursive: true });
  copyFileSync('public/data/placeholder_metric.json', join('dist', 'data', 'placeholder_metric.json'));
}
console.log('Static Phase 0 site built. Replace this compatibility builder with Astro once dependencies are installed.');
