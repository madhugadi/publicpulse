import { getGadgets } from '@/lib/api'
import ItemGrid from '@/components/ItemGrid'

export default async function GadgetsPage() {
  const gadgets = await getGadgets()

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          Gadgets
        </h1>
        <p className="text-muted">
          Understanding how audiences are reacting to recent tech releases
        </p>
      </div>

      <ItemGrid items={gadgets} category="gadgets" />
    </div>
  )
}
