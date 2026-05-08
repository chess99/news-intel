import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import remarkGfm from 'remark-gfm'
import remarkHtml from 'remark-html'

// report/ 目录相对于 site/ 的位置
const REPORT_DIR = path.join(process.cwd(), '..', 'report')

/**
 * 从 markdown 第一个 # 标题中提取标题
 * 若无标题则返回默认值
 */
function extractTitle(content, date) {
  const match = content.match(/^#\s+(.+)$/m)
  return match ? match[1].trim() : `科技资讯日报 · ${date}`
}

/**
 * 从正文中提取前 200 字作为摘要（去除 markdown 标记）
 */
function extractExcerpt(content) {
  const plain = content
    .replace(/^#+\s+.+$/gm, '')      // 去除标题
    .replace(/^>\s+.+$/gm, '')       // 去除引用
    .replace(/\*\*(.+?)\*\*/g, '$1') // 去除加粗
    .replace(/\*(.+?)\*/g, '$1')     // 去除斜体
    .replace(/\n+/g, ' ')            // 合并换行
    .trim()
  return plain.slice(0, 200)
}

/**
 * 返回所有日报的摘要列表，按日期倒序
 * @returns {{ date: string, title: string, excerpt: string }[]}
 */
let _reportsCache = null

export function getAllReports() {
  if (_reportsCache) return _reportsCache
  if (!fs.existsSync(REPORT_DIR)) return []

  _reportsCache = fs
    .readdirSync(REPORT_DIR)
    .filter(f => f.endsWith('.md'))
    .map(f => {
      const date = f.replace('.md', '')
      const raw = fs.readFileSync(path.join(REPORT_DIR, f), 'utf-8')
      const { content } = matter(raw)
      return {
        date,
        title: extractTitle(content, date),
        excerpt: extractExcerpt(content),
      }
    })
    .sort((a, b) => b.date.localeCompare(a.date))

  return _reportsCache
}

/**
 * 返回单篇日报的完整内容
 * @param {string} date  格式 "2026-05-08"
 * @returns {Promise<{ date: string, title: string, htmlContent: string } | null>}
 */
export async function getReport(date) {
  const filePath = path.join(REPORT_DIR, `${date}.md`)
  if (!fs.existsSync(filePath)) return null

  const raw = fs.readFileSync(filePath, 'utf-8')
  const { content } = matter(raw)

  const processed = await remark().use(remarkGfm).use(remarkHtml, { sanitize: false }).process(content)
  const htmlContent = processed.toString()

  return {
    date,
    title: extractTitle(content, date),
    htmlContent,
  }
}
