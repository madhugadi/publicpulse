import Link from 'next/link'
import Image from 'next/image'
import type { Item } from '@/lib/api'
import RatingBar from './RatingBar'

interface ItemCardProps {
  item: Item
}

const categoryAccent: Record<string, string> = {
  movies: 'text-violet-600 group-hover:text-violet-700',
  gadgets: 'text-blue-600 group-hover:text-blue-700',
  vehicles: 'text-amber-600 group-hover:text-amber-700',
}

const categoryBadge: Record<string, string> = {
  movies: 'bg-violet-100 text-violet-700',
  gadgets: 'bg-blue-100 text-blue-700',
  vehicles: 'bg-amber-100 text-amber-700',
}

const categoryPlaceholder: Record<string, string> = {
  movies: 'from-violet-100 to-purple-200',
  gadgets: 'from-blue-100 to-cyan-200',
  vehicles: 'from-amber-100 to-orange-200',
}

export default function ItemCard({ item }: ItemCardProps) {
  const formattedDate = item.last_updated_at
    ? new Date(item.last_updated_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      })
    : null

  const summaryPreview = item.summary
    ? item.summary.slice(0, 140) + (item.summary.length > 140 ? '...' : '')
    : 'No summary available yet.'

  const accent = categoryAccent[item.category] || 'text-slate-600'
  const badge = categoryBadge[item.category] || 'bg-slate-100 text-slate-600'
  const placeholder = categoryPlaceholder[item.category] || 'from-slate-100 to-slate-200'

  return (
    <Link
      href={`/${item.category}/${item.slug}`}
      className="group block bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
    >
      {/* Poster / Placeholder */}
      <div className="relative aspect-[2/3] overflow-hidden">
        {item.poster_url ? (
          <Image
            src={item.poster_url}
            alt={item.title}
            fill
            className="object-cover group-hover:scale-105 transition-transform duration-500"
            sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          />
        ) : (
          <div className={`w-full h-full bg-gradient-to-br ${placeholder} flex items-center justify-center`}>
            <span className="text-8xl font-black select-none opacity-20 text-slate-700">
              {item.title.charAt(0).toUpperCase()}
            </span>
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-transparent" />
        <span className={`absolute top-3 left-3 text-xs font-semibold px-2.5 py-1 rounded-full ${badge}`}>
          {item.category.charAt(0).toUpperCase() + item.category.slice(1)}
        </span>
      </div>

      {/* Content */}
      <div className="p-5">
        <h3 className="text-base font-bold text-slate-900 mb-1 line-clamp-2 leading-snug">
          {item.title}
        </h3>

        {formattedDate && (
          <p className="text-xs text-slate-400 mb-3">Updated {formattedDate}</p>
        )}

        <p className="text-sm text-slate-600 leading-relaxed line-clamp-3 mb-4">
          {summaryPreview}
        </p>

        <RatingBar sentimentCounts={item.sentiment_counts} size="sm" />

        <div className={`mt-4 text-sm font-semibold flex items-center gap-1 ${accent}`}>
          Read analysis
          <span className="group-hover:translate-x-1 transition-transform inline-block">→</span>
        </div>
      </div>
    </Link>
  )
}
