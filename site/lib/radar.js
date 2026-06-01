import fs from 'fs'
import path from 'path'

const ROOT = path.join(process.cwd(), '..')

function readJsonl(filePath) {
  if (!fs.existsSync(filePath)) return []
  return fs.readFileSync(filePath, 'utf-8')
    .split('\n')
    .filter(Boolean)
    .map(line => JSON.parse(line))
}

export function getLatestDailyBriefs(limit = 20) {
  const dir = path.join(ROOT, 'brief', 'daily')
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(name => name.endsWith('.md'))
    .sort()
    .reverse()
    .slice(0, limit)
    .map(name => ({
      date: name.replace('.md', ''),
      markdown: fs.readFileSync(path.join(dir, name), 'utf-8'),
    }))
}

export function getAllEntities() {
  return readJsonl(path.join(ROOT, 'data', 'entities.jsonl'))
}

export function getAllClaims() {
  return readJsonl(path.join(ROOT, 'data', 'claims.jsonl'))
}

export function getAllEvents() {
  const dir = path.join(ROOT, 'data', 'events')
  if (!fs.existsSync(dir)) return []
  return fs.readdirSync(dir)
    .filter(name => name.endsWith('.jsonl'))
    .flatMap(name => readJsonl(path.join(dir, name)))
}

export function getSourceHealth() {
  const filePath = path.join(ROOT, 'state', 'source_health.json')
  if (!fs.existsSync(filePath)) return []
  return Object.values(JSON.parse(fs.readFileSync(filePath, 'utf-8')))
}
