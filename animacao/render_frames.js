// Renderiza os quadros do teste de Short a 12 fps (animação "em dois", estilo stop-motion).
const { chromium } = require('playwright');
const fs = require('fs');
const [svgPath, outDir, nFrames = 96] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.setContent(`<html><head><link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@800&display=block" rel="stylesheet">
    <style>body{margin:0}</style></head><body>${fs.readFileSync(svgPath, 'utf8')}</body></html>`);
  await p.waitForTimeout(1500);
  fs.mkdirSync(outDir, { recursive: true });
  for (let i = 0; i < nFrames; i++) {
    await p.evaluate((i) => {
      const clamp = (x) => Math.max(0, Math.min(1, x));
      const outBack = (t) => { const c = 1.9; return 1 + (c + 1) * Math.pow(t - 1, 3) + c * Math.pow(t - 1, 2); };
      const $ = (id) => document.getElementById(id);
      // tremor de linha: troca o "seed" a cada 2 quadros
      $('turb').setAttribute('seed', [7, 11, 19][Math.floor(i / 2) % 3]);
      // título sendo costurado
      const r = clamp(i / 18), x = 170 + r * 760;
      $('rev').setAttribute('width', r < 1 ? x : 1080);
      $('needle').setAttribute('transform', `translate(${x},330) rotate(${Math.sin(i * 2.1) * 12})`);
      $('needle').style.opacity = r < 1 ? 1 : 0;
      // Gus cai e quica, depois respira
      const g = clamp((i - 10) / 12);
      const y = -900 + outBack(g) * 2010 + (i > 22 ? Math.sin(i / 3) * 8 : 0);
      const rot = i > 22 ? Math.sin(i / 5) * 2.5 : 0;
      $('gus').setAttribute('transform', `translate(540,${y}) rotate(${rot}) scale(1.3) translate(-500,-560)`);
      // balão "psst..." aparece
      const s = i < 30 ? 0 : outBack(clamp((i - 30) / 7));
      $('bub').setAttribute('transform', `translate(-70,40) translate(760,300) scale(${s}) translate(-760,-300)`);
      // etiqueta sobe
      const t = outBack(clamp((i - 42) / 9));
      $('tag').setAttribute('transform', `translate(0,${(1 - t) * 420})`);
    }, i);
    await p.screenshot({ path: `${outDir}/f${String(i).padStart(3, '0')}.png` });
  }
  await b.close();
})();
