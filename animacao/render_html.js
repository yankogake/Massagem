// Renderiza uma página com setT(t, frame) em PNGs a 12 fps.
// Uso: node render_html.js pagina.html pasta_saida duracao_seg [so_quadros_ex: 10,50,100]
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [html, outDir, dur, only] = process.argv.slice(2);
const FPS = 12;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.goto('file://' + path.resolve(html));
  await p.waitForTimeout(2000);
  fs.mkdirSync(outDir, { recursive: true });
  const frames = only ? only.split(',').map(Number) : [...Array(Math.round(dur * FPS)).keys()];
  for (const i of frames) {
    await p.evaluate(([t, i]) => setT(t, i), [i / FPS, i]);
    await p.screenshot({ path: `${outDir}/f${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();
