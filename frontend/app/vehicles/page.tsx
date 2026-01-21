import { getVehicles } from '@/lib/api'
import ItemGrid from '@/components/ItemGrid'

export default async function VehiclesPage() {
  const vehicles = await getVehicles()

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          Vehicles
        </h1>
        <p className="text-muted">
          Understanding how audiences are reacting to recent vehicle releases
        </p>
      </div>

      <ItemGrid items={vehicles} category="vehicles" />
    </div>
  )
}
