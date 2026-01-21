import type { Item } from '@/lib/api'
import ItemCard from './ItemCard'

interface ItemGridProps {
  items: Item[]
  category: string
}

export default function ItemGrid({ items, category }: ItemGridProps) {
  if (items.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted text-lg">
          No {category} available yet.
        </p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {items.map((item) => (
        <ItemCard key={item.slug} item={item} />
      ))}
    </div>
  )
}
