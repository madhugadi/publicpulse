import Link from 'next/link'

const categories = [
  {
    href: '/movies',
    label: 'Movies',
    description: 'Early audience reactions to the latest releases',
    accent: 'from-violet-600 to-purple-700 hover:from-violet-500 hover:to-purple-600',
    ring: 'ring-violet-500',
  },
  {
    href: '/gadgets',
    label: 'Gadgets',
    description: 'What people are saying about new tech',
    accent: 'from-blue-600 to-cyan-700 hover:from-blue-500 hover:to-cyan-600',
    ring: 'ring-blue-500',
  },
  {
    href: '/vehicles',
    label: 'Vehicles',
    description: 'Real-world impressions of new cars & EVs',
    accent: 'from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500',
    ring: 'ring-amber-500',
  },
]

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <div className="relative bg-slate-900 rounded-3xl px-8 py-24 mb-12 overflow-hidden text-center">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_60%_at_50%_0%,rgba(124,58,237,0.25),transparent)]" />
        <div className="relative max-w-3xl mx-auto">
          <span className="inline-block bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-4 py-1.5 text-sm text-white/70 mb-6 tracking-wide">
            Real audience reactions, editorially framed
          </span>
          <h1 className="text-6xl font-extrabold text-white mb-5 tracking-tight">
            Public<span className="text-violet-400">Pulse</span>
          </h1>
          <p className="text-xl text-slate-400 leading-relaxed">
            Understanding how audiences are reacting to movies, gadgets, and vehicles — right now, without hype or scores.
          </p>
        </div>
      </div>

      {/* Category cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {categories.map((cat) => (
          <Link
            key={cat.href}
            href={cat.href}
            className={`group relative bg-gradient-to-br ${cat.accent} rounded-2xl p-8 text-white transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl`}
          >
            <h2 className="text-2xl font-bold mb-2">{cat.label}</h2>
            <p className="text-white/70 text-sm leading-relaxed">{cat.description}</p>
            <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-white/90">
              Explore {cat.label}
              <span className="group-hover:translate-x-1 transition-transform inline-block">→</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
