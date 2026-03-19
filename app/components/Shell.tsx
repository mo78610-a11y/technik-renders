'use client'
import { useState } from 'react'
import Dashboard from './Dashboard'
import IdeaEngine from './IdeaEngine'
import ScriptWriter from './ScriptWriter'
import SEOBuilder from './SEOBuilder'
import ThumbnailBrief from './ThumbnailBrief'
import VoiceoverBrief from './VoiceoverBrief'
import Calendar from './Calendar'
import SOP from './SOP'
import Outreach from './Outreach'

const NAV = [
  { id: 'dashboard',   icon: '▦', label: 'Dashboard'        },
  { id: 'ideas',       icon: '◎', label: 'Idea Engine'       },
  { id: 'script',      icon: '◈', label: 'Script Writer'     },
  { id: 'voiceover',   icon: '◉', label: 'Voiceover Brief'   },
  { id: 'thumbnail',   icon: '◑', label: 'Thumbnail Brief'   },
  { id: 'seo',         icon: '◐', label: 'SEO Builder'       },
  { id: 'calendar',    icon: '▤', label: '30-Day Calendar'   },
  { id: 'sop',         icon: '▣', label: 'Daily SOP'         },
  { id: 'outreach',    icon: '◆', label: 'Sponsor Outreach'  },
]

const VIEWS: Record<string, React.ReactNode> = {
  dashboard: <Dashboard />,
  ideas:     <IdeaEngine />,
  script:    <ScriptWriter />,
  voiceover: <VoiceoverBrief />,
  thumbnail: <ThumbnailBrief />,
  seo:       <SEOBuilder />,
  calendar:  <Calendar />,
  sop:       <SOP />,
  outreach:  <Outreach />,
}

export default function Shell() {
  const [active, setActive] = useState('dashboard')
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="brand-logo">TECHNIK</div>
          <div className="brand-sub">Renders · YT System</div>
        </div>
        <nav className="sidebar-nav">
          {NAV.map(n => (
            <button
              key={n.id}
              className={`nav-item ${active === n.id ? 'active' : ''}`}
              onClick={() => setActive(n.id)}
            >
              <span className="nav-icon">{n.icon}</span>
              {n.label}
            </button>
          ))}
        </nav>
        <div className="sidebar-foot">
          <div className="status-line">
            <div><span className="status-dot" />AI active</div>
            <div style={{ paddingLeft: 11 }}>Claude · Powered</div>
          </div>
        </div>
      </aside>
      <main className="main-panel">
        <div className="fade-up" key={active}>
          {VIEWS[active]}
        </div>
      </main>
    </div>
  )
}
