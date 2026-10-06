// Renderiza video.html quadro a quadro e gera o MP4 com ffmpeg.
// Uso: node tools/renderizar.mjs [saida.mp4]
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { pathToFileURL } from "node:url";
import path from "node:path";

const raiz = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const saida = path.resolve(process.argv[2] ?? path.join(raiz, "harmonie-divulgacao.mp4"));

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(pathToFileURL(path.join(raiz, "video.html")).href + "?render");
await page.evaluate(() => window.pronto);
const { duracao, fps } = await page.evaluate(() => ({ duracao: window.DURACAO, fps: window.FPS }));
const total = Math.round(duracao * fps);

const ffmpeg = spawn("ffmpeg", [
  "-y", "-loglevel", "error",
  "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
  "-c:v", "libx264", "-preset", "slow", "-crf", "17",
  "-pix_fmt", "yuv420p", "-movflags", "+faststart",
  saida,
], { stdio: ["pipe", "inherit", "inherit"] });

const palco = page.locator("#palco");
for (let f = 0; f < total; f++) {
  await page.evaluate(t => window.render(t), f / fps);
  const png = await palco.screenshot({ type: "png" });
  if (!ffmpeg.stdin.write(png)) await new Promise(r => ffmpeg.stdin.once("drain", r));
  if (f % fps === 0) process.stdout.write(`\r${f}/${total} quadros`);
}
ffmpeg.stdin.end();
await new Promise((ok, erro) => ffmpeg.on("close", c => (c === 0 ? ok() : erro(new Error(`ffmpeg saiu com ${c}`)))));
await browser.close();
console.log(`\nPronto: ${saida}`);
