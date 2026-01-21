import { getMovies } from '@/lib/api'
import ItemGrid from '@/components/ItemGrid'

export default async function MoviesPage() {
  const movies = await getMovies()

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-foreground mb-2">
          Movies
        </h1>
        <p className="text-muted">
          Understanding how audiences are reacting to recent releases
        </p>
      </div>

      <ItemGrid items={movies} category="movies" />
    </div>
  )
}
