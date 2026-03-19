import { Link } from 'react-router-dom'
import Reveal from '../components/Reveal'

export default function Credits() {
  return (
    <div className="min-h-[calc(100vh-54px)] bg-ricewhite-100">
      {/* Header Section */}
      <div className="relative bg-ricewhite-50 border-b border-ricewhite-300 overflow-hidden">
        <div className="absolute inset-0 dot-texture opacity-40 pointer-events-none" />
        <div className="relative max-w-5xl mx-auto px-4 sm:px-6 pt-10 pb-8">
          <div className="flex items-center gap-2.5 mb-3">
            <span className="w-4 h-px bg-riceblue-700" />
            <span className="text-xs font-semibold text-riceblue-700 uppercase tracking-[0.16em]">Credits</span>
          </div>
          <h1 className="font-display font-bold text-stone-900 text-3xl sm:text-4xl tracking-tight mb-1.5">
            Built with Purpose
          </h1>
          <p className="text-[15px] text-stone-500">
            RiceResearchFinder was created to connect curious students with world-class faculty.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Creator Section */}
          <Reveal from="left" className="lg:col-span-2">
            <div className="bg-ricewhite-50 rounded-2xl border border-ricewhite-300 p-8 shadow-sm shadow-stone-900/[0.04]">
              <div className="flex items-center gap-2.5 mb-4">
                <span className="w-4 h-px bg-riceblue-700" />
                <span className="text-xs font-semibold text-riceblue-700 uppercase tracking-[0.16em]">Creator</span>
              </div>
              
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="w-16 h-16 rounded-full bg-riceblue-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-riceblue-700 font-display text-xl font-bold">SN</span>
                  </div>
                  <div className="flex-1">
                    <h3 className="font-display font-bold text-stone-900 text-xl mb-1">
                      Shreyas Nirmala Bhaskar
                    </h3>
                    <p className="text-stone-600 text-sm leading-relaxed mb-3">
                      Creator and developer of RiceResearchFinder. Passionate about building tools that bridge the gap between students and research opportunities.
                    </p>
                    <a 
                      href="https://www.linkedin.com/in/shreyas-nirmalabhaskar/" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-1.5 text-[13px] px-4 py-2 bg-riceblue-700 text-ricewhite-100 rounded-lg hover:bg-riceblue-600 transition-colors font-medium"
                    >
                      <svg viewBox="0 0 24 24" fill="currentColor" className="w-4 h-4">
                        <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                      </svg>
                      LinkedIn Profile
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </Reveal>

          {/* Inspiration Section */}
          <Reveal from="right" delay={100}>
            <div className="bg-ricewhite-50 rounded-2xl border border-ricewhite-300 p-8 shadow-sm shadow-stone-900/[0.04]">
              <div className="flex items-center gap-2.5 mb-4">
                <span className="w-4 h-px bg-riceblue-700" />
                <span className="text-xs font-semibold text-riceblue-700 uppercase tracking-[0.16em]">Inspiration</span>
              </div>
              
              <div className="space-y-6">
                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-full bg-riceblue-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-riceblue-700 font-display text-sm font-bold">AV</span>
                  </div>
                  <div className="flex-1">
                    <h4 className="font-display font-bold text-stone-900 text-lg mb-1">Arun Vaithianathan</h4>
                    <a 
                      href="https://www.linkedin.com/in/akvaithi/" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-stone-600 text-sm hover:text-riceblue-700 transition-colors"
                    >
                      LinkedIn Profile
                    </a>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="w-12 h-12 rounded-full bg-riceblue-100 flex items-center justify-center flex-shrink-0">
                    <span className="text-riceblue-700 font-display text-sm font-bold">AM</span>
                  </div>
                  <div className="flex-1">
                    <h4 className="font-display font-bold text-stone-900 text-lg mb-1">Aditya Meenakshisundaram</h4>
                    <a 
                      href="https://www.linkedin.com/in/adityameenakshi/" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-stone-600 text-sm hover:text-riceblue-700 transition-colors"
                    >
                      LinkedIn Profile
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </Reveal>
        </div>

        {/* Project Info Section */}
        <Reveal from="bottom" delay={200} className="mt-12">
          <div className="bg-ricewhite-50 rounded-2xl border border-ricewhite-300 p-8 shadow-sm shadow-stone-900/[0.04]">
            <div className="flex items-center gap-2.5 mb-6">
              <span className="w-4 h-px bg-riceblue-700" />
              <span className="text-xs font-semibold text-riceblue-700 uppercase tracking-[0.16em]">About This Project</span>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-display font-bold text-stone-900 text-lg mb-3">Mission</h3>
                <p className="text-stone-600 text-sm leading-relaxed">
                  To democratize access to research opportunities at Rice University by making it easier for students to discover faculty whose research aligns with their interests and career goals.
                </p>
              </div>
              
              <div>
                <h3 className="font-display font-bold text-stone-900 text-lg mb-3">Technology</h3>
                <p className="text-stone-600 text-sm leading-relaxed">
                  Built with modern web technologies to provide a fast, intuitive, and comprehensive search experience across Rice Engineering faculty profiles.
                </p>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-ricewhite-300">
              <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div className="text-sm text-stone-500">
                  © 2026 RiceResearchFinder. Built for the Rice University community.
                </div>
                <Link 
                  to="/"
                  className="inline-flex items-center gap-1.5 text-sm text-riceblue-700 hover:text-riceblue-600 font-medium transition-colors"
                >
                  <svg viewBox="0 0 20 20" fill="currentColor" className="w-4 h-4">
                    <path fillRule="evenodd" d="M9.293 2.293a1 1 0 011.414 0l7 7a1 1 0 010 1.414l-7 7a1 1 0 01-1.414-1.414L15.586 10H2a1 1 0 110-2h13.586L9.293 3.707a1 1 0 010-1.414z" clipRule="evenodd" />
                  </svg>
                  Back to Home
                </Link>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </div>
  )
}
