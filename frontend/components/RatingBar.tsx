interface SentimentCounts {
  working: number
  mixed: number
  concerns: number
  resonates: number
}

interface RatingBarProps {
  sentimentCounts?: SentimentCounts
  size?: 'sm' | 'md'
}

function calcScore(counts: SentimentCounts): number | null {
  const positive = (counts.working ?? 0) + (counts.resonates ?? 0)
  const total = (counts.working ?? 0) + (counts.mixed ?? 0) + (counts.concerns ?? 0) + (counts.resonates ?? 0)
  if (total === 0) return null
  return Math.round((positive / total) * 100)
}

function getColor(score: number) {
  if (score >= 70) return { bar: 'bg-green-500', text: 'text-green-600', label: 'Positive' }
  if (score >= 40) return { bar: 'bg-yellow-500', text: 'text-yellow-600', label: 'Mixed' }
  return { bar: 'bg-red-500', text: 'text-red-600', label: 'Concerns' }
}

export default function RatingBar({ sentimentCounts, size = 'sm' }: RatingBarProps) {
  if (!sentimentCounts) return null

  const score = calcScore(sentimentCounts)
  if (score === null) return null

  const { bar, text, label } = getColor(score)
  const trackHeight = size === 'md' ? 'h-2.5' : 'h-1.5'
  const textSize = size === 'md' ? 'text-sm' : 'text-xs'
  const total = sentimentCounts.working + sentimentCounts.mixed + sentimentCounts.concerns + sentimentCounts.resonates

  return (
    <div className="w-full">
      <div className={`flex items-center justify-between mb-1.5 ${textSize}`}>
        <span className="text-slate-500 font-medium">
          Audience Sentiment
          {size === 'md' && <span className="text-slate-400 font-normal ml-1">({total} signals)</span>}
        </span>
        <span className={`font-bold ${text}`}>{score}% {label}</span>
      </div>
      <div className={`w-full ${trackHeight} bg-slate-100 rounded-full overflow-hidden`}>
        <div
          className={`${trackHeight} ${bar} rounded-full transition-all duration-500`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  )
}
