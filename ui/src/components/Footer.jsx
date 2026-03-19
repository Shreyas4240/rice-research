import { Link } from 'react-router-dom'

const NAV = [
  { to: '/',         label: 'Home' },
  { to: '/search',   label: 'Search Faculty' },
  { to: '/discover', label: 'Discover Matches' },
  { to: '/saved',    label: 'Saved Professors' },
]

export default function Footer() {
  return (
    <footer className="bg-stone-950 border-t border-stone-800">
      {/* Maroon accent line */}
      <div className="h-[2.5px] bg-riceblue-700" />

      <div className="max-w-6xl mx-auto px-6 sm:px-8 py-14">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-12 mb-12">

          {/* Brand */}
          <div>
            <Link to="/" className="inline-flex items-baseline gap-0.5 mb-4 group select-none">
              <span className="font-display italic text-riceblue-400 text-[20px] font-bold
                               leading-none group-hover:text-riceblue-300 transition-colors">
                Rice
              </span>
              <span className="font-sans font-semibold text-ricewhite-300 text-[14px]
                               tracking-tight group-hover:text-ricewhite-200 transition-colors">
                ResearchFinder
              </span>
            </Link>
            <p className="text-xs text-stone-500 leading-relaxed max-w-[220px]">
              Helping Rice students discover engineering research
              opportunities across all departments, powered by AI matching
              and personalized outreach drafting.
            </p>
          </div>

          {/* Navigation */}
          <div>
            <div className="text-[11px] font-semibold text-stone-500 uppercase
                            tracking-[0.12em] mb-5">
              Navigate
            </div>
            <ul className="space-y-3">
              {NAV.map(({ to, label }) => (
                <li key={to}>
                  <Link
                    to={to}
                    className="text-sm text-stone-400 hover:text-ricewhite-200
                               transition-colors duration-150"
                  >
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Data */}
          <div>
            <div className="text-[11px] font-semibold text-stone-500 uppercase
                            tracking-[0.12em] mb-5">
              Data &amp; Attribution
            </div>
            <p className="text-xs text-stone-500 leading-relaxed">
              Faculty profiles sourced from the Rice College of
              Engineering public directory. AI matching and email drafts
              are generated automatically — always review before sending.
              Not affiliated with or endorsed by Rice University.
            </p>
          </div>
        </div>

        <div className="border-t border-stone-800 pt-7 flex flex-col sm:flex-row
                        items-start sm:items-center justify-between gap-3
                        text-xs text-stone-600">
          <span>&copy; {new Date().getFullYear()} RiceResearchFinder</span>
          <span>Not affiliated with Rice University</span>
        </div>
      </div>
    </footer>
  )
}
