/**
 * API client for PublicPulse backend
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Item {
  title: string
  slug: string
  category: string
  release_date?: string
  last_updated_at: string
  poster_url?: string
  sentiment_counts?: {
    working: number
    mixed: number
    concerns: number
    resonates: number
  }
  buckets: {
    working: string[]
    mixed: string[]
    concerns: string[]
    resonates: string[]
  }
  summary: string
  actor_names?: string[]
}

/**
 * Fetch all movies
 */
export async function getMovies(): Promise<Item[]> {
  const response = await fetch(`${API_BASE}/movies`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Failed to fetch movies')
  }

  return response.json()
}

/**
 * Fetch a specific movie by slug
 */
export async function getMovie(slug: string): Promise<Item> {
  const response = await fetch(`${API_BASE}/movies/${slug}`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Failed to fetch movie')
  }

  return response.json()
}

/**
 * Fetch all gadgets
 */
export async function getGadgets(): Promise<Item[]> {
  const response = await fetch(`${API_BASE}/gadgets`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Failed to fetch gadgets')
  }

  return response.json()
}

/**
 * Fetch a specific gadget by slug
 */
export async function getGadget(slug: string): Promise<Item> {
  const response = await fetch(`${API_BASE}/gadgets/${slug}`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Failed to fetch gadget')
  }

  return response.json()
}

/**
 * Fetch all vehicles
 */
export async function getVehicles(): Promise<Item[]> {
  const response = await fetch(`${API_BASE}/vehicles`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Failed to fetch vehicles')
  }

  return response.json()
}

/**
 * Fetch a specific vehicle by slug
 */
export async function getVehicle(slug: string): Promise<Item> {
  const response = await fetch(`${API_BASE}/vehicles/${slug}`, {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error('Failed to fetch vehicle')
  }

  return response.json()
}
