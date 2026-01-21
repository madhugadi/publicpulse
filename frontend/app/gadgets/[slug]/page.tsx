import { getGadget } from '@/lib/api'
import Link from 'next/link'

interface GadgetPageProps {
  params: {
    slug: string
  }
}

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
    <div>
      <Link
        href="/gadgets"
        className="text-sm text-muted hover:text-foreground mb-4 inline-block"
      >
        ← Back to Gadgets
      </Link>

      <article className="max-w-3xl">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            {gadget.title}
          </h1>
          {formattedDate && (
            <p className="text-sm text-muted">
              Last updated {formattedDate}
            </p>
          )}
        </header>

        {/* Summary */}
        <section className="mb-12">
          <div className="prose prose-lg max-w-none">
            {gadget.summary.split('\n').map((paragraph, idx) => (
              paragraph.trim() && (
                <p key={idx} className="mb-4 text-gray-700 leading-relaxed">
                  {paragraph}
                </p>
              )
            ))}
          </div>
        </section>

        {/* Buckets */}
        <section className="space-y-8">
          {gadget.buckets.working && gadget.buckets.working.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                What seems to be working
              </h2>
              <ul className="space-y-2">
                {gadget.buckets.working.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-green-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {gadget.buckets.mixed && gadget.buckets.mixed.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                Mixed responses
              </h2>
              <ul className="space-y-2">
                {gadget.buckets.mixed.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-yellow-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {gadget.buckets.concerns && gadget.buckets.concerns.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                Emerging concerns
              </h2>
              <ul className="space-y-2">
                {gadget.buckets.concerns.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-red-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {gadget.buckets.resonates && gadget.buckets.resonates.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                Who it seems to be resonating with
              </h2>
              <ul className="space-y-2">
                {gadget.buckets.resonates.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-blue-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </article>
    </div>
  )
}
