import Link from 'next/link'
import { notFound } from 'next/navigation'
import { getAllClaims, getAllEvents } from '../../../lib/radar'

export const dynamicParams = false
export const dynamic = 'force-static'

export async function generateStaticParams() {
  const claims = getAllClaims()
  return claims.length ? claims.map(claim => ({ id: claim.id })) : [{ id: '_empty' }]
}

export default function ClaimPage({ params }) {
  const claim = getAllClaims().find(item => item.id === params.id)
  if (!claim && params.id !== '_empty') notFound()
  if (!claim) {
    return (
      <main className="standalone-page">
        <header className="standalone-header">
          <Link href="/" className="site-logo">Intel Daily</Link>
          <Link href="/topics/" className="header-nav-btn">Topics</Link>
        </header>
        <section className="radar-section">
          <h1>No claims yet</h1>
          <p>Claim pages will appear after the structured radar pipeline has produced data.</p>
        </section>
      </main>
    )
  }
  const events = getAllEvents()
  const byId = Object.fromEntries(events.map(event => [event.id, event]))

  const renderEvents = ids => ids.map(id => byId[id]).filter(Boolean)

  return (
    <main className="standalone-page">
      <header className="standalone-header">
        <Link href="/" className="site-logo">Intel Daily</Link>
        <Link href="/topics/" className="header-nav-btn">Topics</Link>
      </header>
      <section className="radar-section">
        <h1>{claim.title}</h1>
        <p>Status: {claim.status} · Confidence: {claim.confidence}</p>
        <p>{claim.summary}</p>
      </section>
      <ClaimEventSection title="Supporting" events={renderEvents(claim.supporting_event_ids || [])} />
      <ClaimEventSection title="Weakening" events={renderEvents(claim.weakening_event_ids || [])} />
      <ClaimEventSection title="Contradicting" events={renderEvents(claim.contradicting_event_ids || [])} />
    </main>
  )
}

function ClaimEventSection({ title, events }) {
  if (!events.length) return null
  return (
    <section className="radar-section">
      <h2>{title}</h2>
      <ul className="radar-event-list">
        {events.map(event => (
          <li key={event.id}>
            <strong>{event.date} · {event.title}</strong>
            <p>{event.summary}</p>
          </li>
        ))}
      </ul>
    </section>
  )
}
