import { getGadget } from '@/lib/api'
import Link from 'next/link'
import RatingBar from '@/components/RatingBar'

interface GadgetPageProps {
  params: {
    slug: string
  }
}

const buckets = [
  {
    key: 'working' as const,
    label: 'What seems to be working',
    border: 'border-l-green-500',
    badge: 'bg-green-100 text-green-700',
    dot: 'bg-green-500',
  },
  {
    key: 'mixed' as const,
    label: 'Mixed responses',
    border: 'border-l-yellow-500',
    badge: 'bg-yellow-100 text-yellow-700',
    dot: 'bg-yellow-500',
  },
  {
    key: 'concerns' as const,
    label: 'Emerging concerns',
    border: 'border-l-red-500',
    badge: 'bg-red-100 text-red-700',
    dot: 'bg-red-500',
  },
  {
    key: 'resonates' as const,
    label: 'Who it seems to be resonating with',
    border: 'border-l-blue-500',
    badge: 'bg-blue-100 text-blue-700',
    dot: 'bg-blue-500',
  },
]

export default async function GadgetPage({ params }: GadgetPageProps) {
  const gadget = await getGadget(params.slug)

  const formattedDate = gadget.last_updated_at
    ? new Date(gadget.last_updated_at).toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      })
    : null

  return (
    <div className="max-w-4xl mx-auto">
      <Link
        href="/gadgets"
        className="inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-900 mb-6 transition-colors"
      >
        ← Back to Gadgets
      </Link>

      <div className="mb-8">
        <span className="inline-block bg-blue-100 text-blue-700 text-xs font-semibold px-3 py-1 rounded-full mb-3 uppercase tracking-wide">
          Gadget
        </span>
        <h1 className="text-4xl font-extrabold text-slate-900 mb-2 leading-tight">{gadget.title}</h1>
        {formattedDate && (
          <p className="text-sm text-slate-500">Last updated {formattedDate}</p>
        )}
      </div>

      {/* Rating bar */}
      <div className="bg-white rounded-2xl px-8 py-5 shadow-sm mb-6">
        <RatingBar sentimentCounts={gadget.sentiment_counts} size="md" />
      </div>

      <article>
        {/* Summary */}
        <section className="mb-12 bg-white rounded-2xl p-8 shadow-sm">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-5">
            Editorial Summary
          </h2>
          <div className="space-y-4">
            {gadget.summary.split('\n').map((paragraph, idx) =>
              paragraph.trim() ? (
                <p key={idx} className="text-slate-700 leading-relaxed text-[15px]">
                  {paragraph}
                </p>
              ) : null
            )}
          </div>
        </section>

        {/* Buckets */}
        <section className="space-y-5">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-5">
            Audience Signals
          </h2>
          {buckets.map(({ key, label, border, badge, dot }) => {
            const items = gadget.buckets[key]
            if (!items || items.length === 0) return null
            return (
              <div key={key} className={`bg-white rounded-2xl p-6 shadow-sm border-l-4 ${border}`}>
                <div className="flex items-center gap-2 mb-4">
                  <span className={`w-2 h-2 rounded-full ${dot}`} />
                  <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wide">
                    {label}
                  </h3>
                  <span className={`ml-auto text-xs font-semibold px-2 py-0.5 rounded-full ${badge}`}>
                    {items.length}
                  </span>
                </div>
                <ul className="space-y-2.5">
                  {items.map((item, idx) => (
                    <li key={idx} className="text-sm text-slate-700 leading-relaxed flex gap-2">
                      <span className="text-slate-300 mt-1 flex-shrink-0">•</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            )
          })}
        </section>
      </article>
    </div>
  )
}
