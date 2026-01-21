import Link from 'next/link'

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh]">
      <h1 className="text-4xl font-bold text-foreground mb-4">
        PublicPulse
      </h1>
      <p className="text-lg text-muted mb-8 text-center max-w-2xl">
        Editorial intelligence platform that explains how audiences are reacting right now,
        using early public signals.
      </p>
      <div className="flex gap-4">
        <Link
          href="/movies"
          className="px-6 py-3 bg-gray-900 text-white rounded-md hover:bg-gray-800 transition-colors"
        >
          Explore Movies
        </Link>
        <Link
          href="/gadgets"
          className="px-6 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          Explore Gadgets
        </Link>
        <Link
          href="/vehicles"
          className="px-6 py-3 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
        >
          Explore Vehicles
        </Link>
      </div>
    </div>
  )
}
