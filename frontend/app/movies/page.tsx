import { getMovies } from '@/lib/api'
import ItemGrid from '@/components/ItemGrid'

export default async function MoviesPage() {
  const movies = await getMovies()

  return (
    <div>
      <div className="mb-10">
        <span className="inline-block bg-violet-100 text-violet-700 text-xs font-semibold px-3 py-1 rounded-full mb-3 uppercase tracking-wide">
          Movies
        </span>
        <h1 className="text-4xl font-extrabold text-slate-900 mb-2 tracking-tight">
          Audience Reactions
        </h1>
        <p className="text-slate-500 text-lg">
          Understanding how audiences are reacting to recent releases
        </p>
      </div>

      <ItemGrid items={movies} category="movies" />
    </div>
  )
}
