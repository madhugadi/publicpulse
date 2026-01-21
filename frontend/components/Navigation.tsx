'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navigation() {
  const pathname = usePathname()

  const isActive = (path: string) => {
    return pathname.startsWith(path)
  }

  return (
    <nav className="border-b border-border bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-semibold text-foreground">
              PublicPulse
            </Link>
            <div className="ml-10 flex items-baseline space-x-4">
              <Link
                href="/movies"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/movies')
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Movies
              </Link>
              <Link
                href="/gadgets"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/gadgets')
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Gadgets
              </Link>
              <Link
                href="/vehicles"
                className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive('/vehicles')
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                Vehicles
              </Link>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
