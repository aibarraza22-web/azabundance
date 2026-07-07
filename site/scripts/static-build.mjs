import { mkdirSync, copyFileSync, writeFileSync, rmSync, existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';

function loadJson(path, fallback = []) {
  return existsSync(path) ? JSON.parse(readFileSync(path, 'utf8')) : fallback;
}

const components = loadJson('public/data/index_components.json');
const housing = loadJson('public/data/housing_permits_quarterly.json');
const datacenters = loadJson('public/data/datacenter_load.json');

function shell(title, h1, body, content = '') {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>${title}</title><style>:root{color:#17202a;background:#fbfaf7;font-family:Inter,ui-sans-serif,system-ui,sans-serif;--accent:#9a3412}body{margin:0}header,main,footer{max-width:1080px;margin:0 auto;padding:1.25rem}header{border-bottom:1px solid #e5e1d8;display:flex;justify-content:space-between;gap:1rem;align-items:center}nav{display:flex;flex-wrap:wrap;gap:.75rem}a{color:var(--accent)}.brand{color:#17202a;font-weight:800;text-decoration:none}h1{font-size:clamp(2.2rem,5vw,4.75rem);line-height:.95;max-width:900px;letter-spacing:-.05em}.lede{font-size:1.25rem;line-height:1.6;max-width:760px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}.card{background:white;border:1px solid #e5e1d8;border-radius:16px;padding:1.25rem}.kpi{font-size:2.4rem;font-weight:850;letter-spacing:-.04em}.meta{color:#5f6b75;font-size:.92rem}table{border-collapse:collapse;width:100%;background:white}td,th{border-bottom:1px solid #e5e1d8;text-align:left;padding:.6rem}</style></head><body><header><a class="brand" href="/">Arizona Abundance Index</a><nav><a href="/index/">Index</a><a href="/methodology/">Methodology</a><a href="/data/">Data</a><a href="/essays/">Essays</a><a href="/about/">About</a></nav></header><main><h1>${h1}</h1><p class="lede">${body}</p>${content}</main><footer>Built for reproducible, methodology-transparent data journalism.</footer></body></html>`;
}

function indexCards() {
  const latestHousing = housing.filter((r) => r.period === '2026-Q2').sort((a, b) => b.value - a.value);
  const latestDc = datacenters.sort((a, b) => a.status.localeCompare(b.status));
  const housingCards = latestHousing.map((r) => `<article class="card"><h2>${r.geography}</h2><div class="kpi">${Number(r.value).toLocaleString()}</div><p>Housing units permitted in ${r.period} to date.</p><p class="meta">Vintage ${r.vintage_date}. Source: <a href="${r.source_url}">FRED/Census</a>.</p></article>`).join('');
  const dcCards = latestDc.map((r) => `<article class="card"><h2>Data centers: ${r.status}</h2><div class="kpi">${Number(r.value).toLocaleString()} MW</div><p>${r.geography}, ${r.period}.</p><p class="meta">${r.method_note} <a href="${r.source_url}">Source document</a>.</p></article>`).join('');
  return `<section class="grid">${housingCards}${dcCards}</section><p><a href="/data/index_components.json">Download component JSON</a> · <a href="/data/index_components.csv">Download component CSV</a> · <a href="/methodology/">Read methodology</a></p>`;
}

function dataTable(rows) {
  return `<table><thead><tr><th>Metric</th><th>Period</th><th>Geography</th><th>Value</th></tr></thead><tbody>${rows.map((r) => `<tr><td>${r.metric}</td><td>${r.period}</td><td>${r.geography}</td><td>${r.value}</td></tr>`).join('')}</tbody></table>`;
}

const pages = [
  ['dist/index.html', 'Arizona Abundance Index', 'Is Arizona actually building?', 'A quarterly, methodology-transparent scoreboard for Arizona housing, energy, chips, data centers, and permitting capacity.', '<p><a href="/index/">View the current component index</a></p>'],
  ['dist/index/index.html', 'Scoreboard | Arizona Abundance Index', 'Arizona Abundance Index', 'Current Phase 1 component data. No composite index is published until at least eight quarters of validated history exist.', indexCards()],
  ['dist/methodology/index.html', 'Methodology | Arizona Abundance Index', 'Methodology', 'Every published number traces to snapshotted raw data, validated tidy rows, and a documented source/vintage.', '<p>Current live components: Census BPS housing permits via FRED-hosted Census series; hand-curated Arizona data center load with primary-document URL per row.</p>'],
  ['dist/data/index.html', 'Data | Arizona Abundance Index', 'Data downloads', 'Static CSV and JSON outputs published after validation.', `${dataTable(components)}<ul><li><a href="/data/housing_permits_quarterly.json">Housing permits quarterly JSON</a></li><li><a href="/data/datacenter_load.json">Data center load JSON</a></li><li><a href="/data/figure_manifest.json">Figure manifest JSON</a></li></ul>`],
  ['dist/essays/index.html', 'Essays | Arizona Abundance Index', 'Essays', 'Essay infrastructure is reserved for the project owner. Every number in future essays must come from the pipeline.', ''],
  ['dist/about/index.html', 'About | Arizona Abundance Index', 'About', 'About page copy is intentionally reserved for the project owner.', ''],
];

rmSync('dist', { recursive: true, force: true });
for (const [path, title, h1, body, content] of pages) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, shell(title, h1, body, content));
}
if (existsSync('public/data')) {
  mkdirSync(join('dist', 'data'), { recursive: true });
  for (const file of ['index_components.json', 'index_components.csv', 'housing_permits_monthly.json', 'housing_permits_quarterly.json', 'datacenter_load.json', 'figure_manifest.json']) {
    const publicPath = join('public', 'data', file);
    const publishedPath = join('..', 'data', 'published', file);
    if (existsSync(publicPath)) copyFileSync(publicPath, join('dist', 'data', file));
    else if (existsSync(publishedPath)) copyFileSync(publishedPath, join('dist', 'data', file));
  }
}
console.log('Static site built with validated component data.');
