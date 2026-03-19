'use client'

const TOOLS = [
  { name: 'Claude',          url: 'https://claude.ai',                          cat: 'AI Brain'    },
  { name: 'ElevenLabs',      url: 'https://elevenlabs.io',                      cat: 'Voice'       },
  { name: 'Higgsfield',      url: 'https://higgsfield.ai',                      cat: 'Video'       },
  { name: 'Invideo AI',      url: 'https://invideo.io',                         cat: 'Video'       },
  { name: 'Runway ML',       url: 'https://runwayml.com',                       cat: 'Video'       },
  { name: 'Midjourney',      url: 'https://midjourney.com',                     cat: 'Renders'     },
  { name: 'Canva',           url: 'https://canva.com',                          cat: 'Thumbnails'  },
  { name: 'VidIQ',           url: 'https://vidiq.com',                          cat: 'SEO'         },
  { name: 'TubeBuddy',       url: 'https://tubebuddy.com',                      cat: 'SEO'         },
  { name: 'Zapier',          url: 'https://zapier.com',                         cat: 'Automation'  },
  { name: 'Gumroad',         url: 'https://gumroad.com',                        cat: 'Revenue'     },
  { name: 'Stan Store',      url: 'https://stan.store',                         cat: 'Revenue'     },
]

const PIPELINE = [
  { step: '01', label: 'Topic',      tool: 'Claude + VidIQ',        time: '5 min'  },
  { step: '02', label: 'Script',     tool: 'Claude',                time: '10 min' },
  { step: '03', label: 'Voiceover',  tool: 'ElevenLabs',            time: '5 min'  },
  { step: '04', label: 'Renders',    tool: 'Midjourney / Higgsfield',time: '15 min' },
  { step: '05', label: 'Video Edit', tool: 'Invideo AI',            time: '10 min' },
  { step: '06', label: 'Thumbnail',  tool: 'Midjourney + Canva',    time: '10 min' },
  { step: '07', label: 'SEO',        tool: 'Claude + VidIQ',        time: '10 min' },
  { step: '08', label: 'Upload',     tool: 'YouTube Studio',        time: '5 min'  },
  { step: '09', label: 'Distribute', tool: 'Zapier',                time: '0 min'  },
]

function Tag({ text, type = 'gray' }: { text: string; type?: string }) {
  return <span className={`tag tag-${type}`}>{text}</span>
}

export default function Dashboard() {
  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <div style={{ fontFamily: 'var(--font-display)', fontSize: 52, letterSpacing: '0.04em', lineHeight: 1, color: 'var(--text)', marginBottom: 4 }}>
          TECHNIK RENDERS
        </div>
        <div style={{ fontFamily: 'var(--font-mono)', fontSize: 11, color: 'var(--gold)', letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 12 }}>
          YouTube Automation Control Center
        </div>
        <p style={{ color: 'var(--text2)', fontSize: 13, maxWidth: 520 }}>
          Cinematic automotive content — faceless, AI-generated, fully automated.
          Luxury renders. Zero recording. Zero editing. Zero burnout.
        </p>
      </div>

      {/* Metrics */}
      <div className="metrics-grid">
        {[
          { label: 'Daily revenue target', value: '$50K',  sub: 'all streams stacked' },
          { label: 'Videos per day',        value: '1–3',  sub: 'fully automated'     },
          { label: 'Human time needed',     value: '1 HR', sub: 'review & approve'    },
          { label: 'Revenue streams',       value: '4',    sub: 'AdSense · Affiliate · Sponsor · Product' },
        ].map(m => (
          <div className="metric-card" key={m.label}>
            <div className="metric-label">{m.label}</div>
            <div className="metric-value">{m.value}</div>
            <div className="metric-sub">{m.sub}</div>
          </div>
        ))}
      </div>

      {/* Pipeline */}
      <div className="section-block">
        <p className="eyebrow gold">Production pipeline</p>
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {PIPELINE.map((p, i) => (
            <div key={p.step} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <div className="card-sm" style={{ minWidth: 120 }}>
                <div style={{ fontFamily: 'var(--font-mono)', fontSize: 9, color: 'var(--gold)', letterSpacing: '0.1em', marginBottom: 6 }}>{p.step}</div>
                <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>{p.label}</div>
                <div style={{ fontSize: 11, color: 'var(--text2)', marginBottom: 6 }}>{p.tool}</div>
                <Tag text={p.time} type="gray" />
              </div>
              {i < PIPELINE.length - 1 && (
                <span style={{ color: 'var(--text3)', fontSize: 12 }}>→</span>
              )}
            </div>
          ))}
        </div>
      </div>

      <hr className="divider" />

      {/* Revenue streams */}
      <div className="section-block">
        <p className="eyebrow gold">Revenue streams</p>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit,minmax(200px,1fr))', gap: 10 }}>
          {[
            { name: 'AdSense',         badge: '$8–$25 RPM',      note: 'Auto/finance niche. Scales with views.',          col: 'gold'  },
            { name: 'Sponsorships',    badge: '$2k–$20k/video',  note: 'Highest earner. Target at 10k+ subs.',            col: 'blue'  },
            { name: 'Affiliate links', badge: 'Passive income',  note: 'Amazon + detailing products in every desc.',      col: 'green' },
            { name: 'Digital product', badge: '100% margin',     note: 'PPF guide, detailing SOP, course via Gumroad.',   col: 'gray'  },
          ].map(s => (
            <div className="card-sm" key={s.name}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                <span style={{ fontSize: 13, fontWeight: 600 }}>{s.name}</span>
                <Tag text={s.badge} type={s.col} />
              </div>
              <div style={{ fontSize: 12, color: 'var(--text2)' }}>{s.note}</div>
            </div>
          ))}
        </div>
      </div>

      <hr className="divider" />

      {/* Tool Stack */}
      <div className="section-block">
        <p className="eyebrow gold">Full AI tool stack</p>
        <div className="tool-grid">
          {TOOLS.map(t => (
            <a key={t.name} href={t.url} target="_blank" rel="noreferrer" className="tool-chip">
              <span style={{ color: 'var(--gold)', fontSize: 10 }}>↗</span>
              {t.name}
              <Tag text={t.cat} type="gray" />
            </a>
          ))}
        </div>
      </div>
    </div>
  )
}
