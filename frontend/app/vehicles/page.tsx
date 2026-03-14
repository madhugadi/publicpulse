import { getVehicles } from '@/lib/api'
import ItemGrid from '@/components/ItemGrid'

export default async function VehiclesPage() {
  const vehicles = await getVehicles()

  return (
    <div>
      <div className="mb-10">
        <span className="inline-block bg-amber-100 text-amber-700 text-xs font-semibold px-3 py-1 rounded-full mb-3 uppercase tracking-wide">
          Vehicles
        </span>
        <h1 className="text-4xl font-extrabold text-slate-900 mb-2 tracking-tight">
          Audience Reactions
        </h1>
        <p className="text-slate-500 text-lg">
          Understanding how audiences are reacting to recent vehicle releases
        </p>
      </div>

      <ItemGrid items={vehicles} category="vehicles" />
    </div>
  )
}
