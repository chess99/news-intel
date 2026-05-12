#!/usr/bin/env node
/**
 * git_push.js — 用 GitHub App token 推送 news-intel 到 chess99/news-intel
 */
const https = require("https");
const crypto = require("crypto");
const fs = require("fs");
const { execSync } = require("child_process");

const APP_ID = "3056722";
const KEY_PATH = "/root/.openclaw/chess99-openclaw.2026-03-10.private-key.pem";
const REPO = "chess99/news-intel";
const WORKDIR = "/root/.openclaw/workspace/news-intel";

function makeJwt() {
  const privateKey = fs.readFileSync(KEY_PATH, "utf8");
  const now = Math.floor(Date.now() / 1000);
  const header = Buffer.from(JSON.stringify({ alg: "RS256", typ: "JWT" })).toString("base64url");
  const payload = Buffer.from(JSON.stringify({ iat: now - 60, exp: now + 540, iss: APP_ID })).toString("base64url");
  const msg = header + "." + payload;
  const sig = crypto.createSign("RSA-SHA256").update(msg).sign(privateKey);
  return msg + "." + Buffer.from(sig).toString("base64url");
}

function ghReq(method, path, token, body) {
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: "api.github.com", path, method,
      headers: {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "openclaw-news-intel",
        "Content-Type": "application/json"
      }
    }, res => {
      let d = "";
      res.on("data", c => d += c);
      res.on("end", () => resolve({ status: res.statusCode, body: JSON.parse(d) }));
    });
    req.on("error", reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

(async () => {
  const jwt = makeJwt();
  const inst = await ghReq("GET", "/app/installations", jwt);
  const chess99 = inst.body.find(i => i.account && i.account.login === "chess99");
  if (!chess99) { console.error("chess99 installation not found"); process.exit(1); }
  const tok = await ghReq("POST", `/app/installations/${chess99.id}/access_tokens`, jwt);
  const token = tok.body.token;

  const url = `https://x-access-token:${token}@github.com/${REPO}.git`;
  const proxy = "http://127.0.0.1:7890";
  execSync(`git -c http.proxy='' -c https.proxy='' remote set-url origin ${url}`, { cwd: WORKDIR, stdio: "inherit" });

  // push 前先 pull rebase，防止本地落后远端导致 non-fast-forward
  try {
    execSync(`git -c http.proxy=${proxy} -c https.proxy=${proxy} pull --rebase origin main`, { cwd: WORKDIR, stdio: "pipe" });
  } catch (e) {
    console.log("pull rebase 失败（可能无网络），继续尝试 push...");
  }

  // 先尝试直连，失败再走代理
  try {
    execSync(`git -c http.proxy='' -c https.proxy='' push origin main`, { cwd: WORKDIR, stdio: "inherit" });
  } catch (e) {
    console.log("直连失败，尝试代理...");
    execSync(`git -c http.proxy=${proxy} -c https.proxy=${proxy} push origin main`, { cwd: WORKDIR, stdio: "inherit" });
  }
  console.log("push ok");
})().catch(e => { console.error(e.message); process.exit(1); });
