import { getMovie } from '@/lib/api'
import Link from 'next/link'

interface MoviePageProps {
  params: {
    slug: string
  }
}

export default async function MoviePage({ params }: MoviePageProps) {
  const movie = await getMovie(params.slug)

  const formattedDate = movie.last_updated_at
    ? new Date(movie.last_updated_at).toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
        year: 'numeric',
      })
    : null

  return (
    <div>
      <Link
        href="/movies"
        className="text-sm text-muted hover:text-foreground mb-4 inline-block"
      >
        ← Back to Movies
      </Link>

      <article className="max-w-3xl">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-foreground mb-2">
            {movie.title}
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
            {movie.summary.split('\n').map((paragraph, idx) => (
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
          {movie.buckets.working && movie.buckets.working.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                What seems to be working
              </h2>
              <ul className="space-y-2">
                {movie.buckets.working.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-green-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {movie.buckets.mixed && movie.buckets.mixed.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                Mixed responses
              </h2>
              <ul className="space-y-2">
                {movie.buckets.mixed.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-yellow-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {movie.buckets.concerns && movie.buckets.concerns.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                Emerging concerns
              </h2>
              <ul className="space-y-2">
                {movie.buckets.concerns.map((item, idx) => (
                  <li key={idx} className="text-gray-700 pl-4 border-l-2 border-red-500">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {movie.buckets.resonates && movie.buckets.resonates.length > 0 && (
            <div>
              <h2 className="text-xl font-semibold text-foreground mb-3">
                Who it seems to be resonating with
              </h2>
              <ul className="space-y-2">
                {movie.buckets.resonates.map((item, idx) => (
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
