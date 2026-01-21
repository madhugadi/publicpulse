import Link from 'next/link'
import type { Item } from '@/lib/api'

interface ItemCardProps {
  item: Item
}

export default function ItemCard({ item }: ItemCardProps) {
  // Format date
  const formattedDate = item.last_updated_at
    ? new Date(item.last_updated_at).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
      })
    : null

  // Get preview of summary (first 150 characters)
  const summaryPreview = item.summary
    ? item.summary.slice(0, 150) + (item.summary.length > 150 ? '...' : '')
    : 'No summary available yet.'

  return (
    <Link
      href={`/${item.category}/${item.slug}`}
      className="block bg-white border border-border rounded-lg p-6 hover:shadow-md transition-shadow"
    >
      <div className="flex flex-col h-full">
        <h3 className="text-lg font-semibold text-foreground mb-2">
          {item.title}
        </h3>

        {formattedDate && (
          <p className="text-xs text-muted mb-3">
            Updated {formattedDate}
          </p>
        )}

        <p className="text-sm text-gray-700 leading-relaxed mb-4 flex-grow">
          {summaryPreview}
        </p>

        <div className="text-sm font-medium text-gray-900">
          Read more →
        </div>
      </div>
    </Link>
  )
}
