// Renderiza video.html quadro a quadro, gera a trilha sonora e junta tudo no MP4.
// Uso: node tools/renderizar.mjs [saida.mp4]
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import { mkdtempSync, writeFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { pathToFileURL } from "node:url";
import path from "node:path";

const raiz = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const saida = path.resolve(process.argv[2] ?? path.join(raiz, "harmonie-divulgacao.mp4"));
const tmp = mkdtempSync(path.join(tmpdir(), "harmonie-"));
const videoMudo = path.join(tmp, "video.mp4");
const roteiroSom = path.join(tmp, "som.json");
const trilha = path.join(tmp, "trilha.wav");

function roda(cmd, args, opcoes = {}) {
  const p = spawn(cmd, args, { stdio: ["pipe", "inherit", "inherit"], ...opcoes });
  p.fim = new Promise((ok, erro) => p.on("close", c => (c === 0 ? ok() : erro(new Error(`${cmd} saiu com ${c}`)))));
  return p;
}

// 1) quadros -> vídeo sem áudio (com granulação leve de filme)
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(pathToFileURL(path.join(raiz, "video.html")).href + "?render");
await page.evaluate(() => window.pronto);
const { duracao, fps, som } = await page.evaluate(() => ({ duracao: window.DURACAO, fps: window.FPS, som: window.SOM }));
writeFileSync(roteiroSom, JSON.stringify(som));
const total = Math.round(duracao * fps);

const ffmpeg = roda("ffmpeg", [
  "-y", "-loglevel", "error",
  "-f", "image2pipe", "-framerate", String(fps), "-i", "-",
  "-vf", "noise=alls=3:allf=t",
  "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-maxrate", "12M", "-bufsize", "24M",
  "-profile:v", "high", "-pix_fmt", "yuv420p",
  videoMudo,
]);
const palco = page.locator("#palco");
for (let f = 0; f < total; f++) {
  await page.evaluate(t => window.render(t), f / fps);
  const png = await palco.screenshot({ type: "png" });
  if (!ffmpeg.stdin.write(png)) await new Promise(r => ffmpeg.stdin.once("drain", r));
  if (f % fps === 0) process.stdout.write(`\r${f}/${total} quadros`);
}
ffmpeg.stdin.end();
await ffmpeg.fim;
await browser.close();
console.log(`\r${total}/${total} quadros`);

// 2) trilha sonora sincronizada
await roda("python3", [path.join(raiz, "tools", "trilha.py"), roteiroSom, trilha], { stdio: "inherit" }).fim;

// 3) mixagem final: áudio normalizado para redes sociais (-14 LUFS)
await roda("ffmpeg", [
  "-y", "-loglevel", "error",
  "-i", videoMudo, "-i", trilha,
  "-map", "0:v", "-map", "1:a",
  "-c:v", "copy",
  "-af", "loudnorm=I=-14:TP=-1:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
  "-shortest", "-movflags", "+faststart",
  saida,
], { stdio: "inherit" }).fim;

rmSync(tmp, { recursive: true, force: true });
console.log(`Pronto: ${saida}`);
