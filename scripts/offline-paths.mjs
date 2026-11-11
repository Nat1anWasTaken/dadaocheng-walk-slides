// Rewrite root-relative /images/ paths so the offline build opens from file://
import { readFileSync, rmSync, writeFileSync } from 'node:fs'

const dir = process.argv[2] ?? 'offline'
const file = `${dir}/index.html`
const html = readFileSync(file, 'utf8').replace(/([`"'(])\/images\//g, '$1./images/')
writeFileSync(file, html)

// Server-only files from public/ and the build
for (const name of ['404.html', '_redirects'])
  rmSync(`${dir}/${name}`, { force: true })
