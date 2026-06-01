import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getAllEntities, getAllEvents } from '../../../lib/radar'

export const dynamicParams = false
export const dynamic = 'force-static'

export async function generateStaticParams() {
  const entities = getAllEntities()
  return entities.length ? entities.map(entity => ({ id: entity.id })) : [{ id: '_empty' }]
}

export default function EntityPage({ params }) {
  const entity = getAllEntities().find(item => item.id === params.id)
  if (!entity && params.id !== '_empty') notFound()
  if (!entity) {
    return (
      <main className="standalone-page">
        <header className="standalone-header">
          <Link href="/" className="site-logo">Intel Daily</Link>
          <Link href="/topics/" className="header-nav-btn">Topics</Link>
        </header>
        <section className="radar-section">
          <h1>No entities yet</h1>
          <p>Entity timelines will appear after the structured radar pipeline has produced data.</p>
        </section>
      </main>
    )
  }
  const events = getAllEvents()
    .filter(event => event.entity_ids?.includes(entity.id))
    .sort((a, b) => b.date.localeCompare(a.date))

  return (
    <main className="standalone-page">
      <header className="standalone-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <Link href="/topics/" className="header-nav-btn">Topics</Link>
      </header>
      <section className="radar-section">
        <h1>{entity.name}</h1>
        <p>{entity.kind} · {events.length} tracked events</p>
      </section>
      <section className="radar-section">
        <h2>Timeline</h2>
        <ul className="radar-event-list">
          {events.map(event => (
            <li key={event.id}>
              <strong>{event.date} · {event.title}</strong>
              <p>{event.summary}</p>
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
