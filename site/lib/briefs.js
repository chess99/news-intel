import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import remarkGfm from 'remark-gfm'
import remarkHtml from 'remark-html'

const BRIEF_DIR = path.join(process.cwd(), '..', 'brief', 'daily')

function extractTitle(content, date) {
  const match = content.match(/^#\s+(.+)$/m)
  return match ? match[1].trim() : `Personal Tech Radar · ${date}`
}

function extractExcerpt(content) {
  const plain = content
    .replace(/^#+\s+.+$/gm, '')
    .replace(/^>\s+.+$/gm, '')
    .replace(/\*\*(.+?)\*\*/g, '$1')
    .replace(/\*(.+?)\*/g, '$1')
    .replace(/\n+/g, ' ')
    .trim()
  return plain.slice(0, 200)
}

let briefsCache = null

export function getAllBriefs() {
  if (briefsCache) return briefsCache
  if (!fs.existsSync(BRIEF_DIR)) return []

  briefsCache = fs
    .readdirSync(BRIEF_DIR)
    .filter(file => file.endsWith('.md'))
    .map(file => {
      const date = file.replace('.md', '')
      const raw = fs.readFileSync(path.join(BRIEF_DIR, file), 'utf-8')
      const { content } = matter(raw)
      return {
        date,
        title: extractTitle(content, date),
        excerpt: extractExcerpt(content),
      }
    })
    .sort((a, b) => b.date.localeCompare(a.date))

  return briefsCache
}

export async function getBrief(date) {
  const filePath = path.join(BRIEF_DIR, `${date}.md`)
  if (!fs.existsSync(filePath)) return null

  const raw = fs.readFileSync(filePath, 'utf-8')
  const { content } = matter(raw)
  const processed = await remark().use(remarkGfm).use(remarkHtml, { sanitize: false }).process(content)

  return {
    date,
    title: extractTitle(content, date),
    htmlContent: processed.toString(),
  }
}
