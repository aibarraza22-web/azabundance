import { existsSync } from 'node:fs';

const required = [
  'src/pages/index.astro',
  'src/pages/index/index.astro',
  'src/pages/methodology/index.astro',
  'src/pages/data/index.astro',
  'src/pages/essays/index.astro',
  'src/pages/about/index.astro',
];

const missing = required.filter((path) => !existsSync(new URL(`../${path}`, import.meta.url)));
if (missing.length) {
  console.error(`Missing required pages: ${missing.join(', ')}`);
  process.exit(1);
}
console.log('Required Astro pages are present.');
