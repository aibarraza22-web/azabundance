import { existsSync, readFileSync } from 'node:fs';
const required = ['dist/index.html', 'dist/style.css', 'dist/app.js'];
for (const path of required) {
  if (!existsSync(path)) throw new Error(`Missing ${path}`);
}
const html = readFileSync('dist/index.html', 'utf8');
const js = readFileSync('dist/app.js', 'utf8');
for (const label of ['Bottled water production', 'CBS News', 'Poll analysis']) {
  if (!html.includes(label) && !js.includes(label)) throw new Error(`Missing required content: ${label}`);
}
console.log('All Water Guess pages and required content passed.');
