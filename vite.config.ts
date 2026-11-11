import type { Plugin } from 'vite'
import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

// Slidev splits vendor chunks, which can't coexist with one inlined bundle
const dropManualChunks: Plugin = {
  name: 'offline:drop-manual-chunks',
  enforce: 'post',
  configResolved(config) {
    const output = config.build.rollupOptions.output
    for (const o of Array.isArray(output) ? output : [output])
      if (o) delete o.manualChunks
  },
}

// `pnpm build:offline` sets OFFLINE=1 to bundle the deck into one HTML file
// that opens from file:// without a server
export default defineConfig({
  plugins: process.env.OFFLINE
    ? [viteSingleFile({ removeViteModuleLoader: true }), dropManualChunks]
    : [],
})
