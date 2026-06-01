import Link from 'next/link'
import { getAllClaims, getAllEntities, getAllEvents } from '../../lib/radar'

export const metadata = {
  title: 'Radar Topics',
  description: 'Personal Tech Radar tracked entities, claims, and event timelines.',
}

export default function TopicsPage() {
  const claims = getAllClaims()
  const entities = getAllEntities()
  const events = getAllEvents().sort((a, b) => b.date.localeCompare(a.date)).slice(0, 30)

  return (
    <main className="standalone-page">
      <header className="standalone-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <span className="site-tagline">Personal Tech Radar</span>
      </header>
      <section className="radar-section">
        <h1>Topics</h1>
        <p>Tracked claims, entities, and recent evidence-backed events.</p>
      </section>
      <section className="radar-section">
        <h2>Claims</h2>
        <ul className="radar-list">
          {claims.map(claim => (
            <li key={claim.id}>
              <Link href={`/claims/${claim.id}/`}>{claim.title}</Link>
              <span>{claim.status} · {claim.confidence}</span>
            </li>
          ))}
        </ul>
      </section>
      <section className="radar-section">
        <h2>Entities</h2>
        <ul className="radar-list">
          {entities.map(entity => (
            <li key={entity.id}>
              <Link href={`/entities/${entity.id}/`}>{entity.name}</Link>
              <span>{entity.event_ids?.length || 0} events</span>
            </li>
          ))}
        </ul>
      </section>
      <section className="radar-section">
        <h2>Recent Events</h2>
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
