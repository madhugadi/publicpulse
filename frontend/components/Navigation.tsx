'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export default function Navigation() {
  const pathname = usePathname()

  const isActive = (path: string) => pathname.startsWith(path)

  return (
    <nav className="sticky top-0 z-50 bg-slate-900 border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link href="/" className="flex items-center gap-1">
            <span className="text-xl font-extrabold text-white tracking-tight">
              Public<span className="text-violet-400">Pulse</span>
            </span>
          </Link>

          <div className="flex items-center gap-1">
            <Link
              href="/movies"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/movies')
                  ? 'bg-violet-600 text-white'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              Movies
            </Link>
            <Link
              href="/gadgets"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/gadgets')
                  ? 'bg-blue-600 text-white'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              Gadgets
            </Link>
            <Link
              href="/vehicles"
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                isActive('/vehicles')
                  ? 'bg-amber-600 text-white'
                  : 'text-slate-300 hover:text-white hover:bg-slate-800'
              }`}
            >
              Vehicles
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
