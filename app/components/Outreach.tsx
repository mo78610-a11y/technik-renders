'use client'
import { useState } from 'react'
import AIModule from './AIModule'

const TYPES = [
  { id: 'ppf',       label: 'PPF / car protection brand' },
  { id: 'detailing', label: 'Detailing product'           },
  { id: 'insurance', label: 'Insurance / finance'         },
  { id: 'tech',      label: 'Dashcam / car tech'          },
  { id: 'luxury',    label: 'Luxury lifestyle brand'      },
  { id: 'affiliate', label: 'Affiliate upgrade'           },
]

export default function Outreach() {
  const [type, setType] = useState('ppf')

  return (
    <div>
      <h1 className="page-title">Sponsor Outreach</h1>
      <p className="page-sub">
        Cold emails for brand deals. Generate, personalise, send.
        Start outreach at 5k subscribers. One email per week minimum.
      </p>

      <p className="eyebrow gold" style={{ marginBottom: 10 }}>Sponsor type</p>
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 24 }}>
        {TYPES.map(t => (
          <button
            key={t.id}
            className={`btn btn-ghost ${type === t.id ? 'sel' : ''}`}
            style={{ padding: '7px 14px', fontSize: 12 }}
            onClick={() => setType(t.id)}
          >
            {t.label}
          </button>
        ))}
      </div>

      <AIModule
        title=""
        subtitle=""
        outputLabel="Generate Email"
        fields={[
          { id: 'channel',  placeholder: 'Channel name',                       default: 'Technik Renders', flex: 1 },
          { id: 'subs',     placeholder: 'Subscribers (e.g. 12,500)',           flex: 1 },
          { id: 'views',    placeholder: 'Avg views per video (e.g. 8,000)',    flex: 1 },
          { id: 'brand',    placeholder: 'Brand / company name (optional)',     flex: 1 },
        ]}
        system={`You are a YouTube sponsorship outreach specialist writing for "Technik Renders" — a cinematic automotive channel producing AI-rendered luxury car content. You write confident, concise cold emails under 180 words that get replies. Peer-to-peer tone, never desperate. Always include a compelling subject line.`}
        promptFn={v => `Write a cold sponsor outreach email for Technik Renders.

Channel: ${v.channel || 'Technik Renders'}
Subscribers: ${v.subs || '[X,000]'}
Average views per video: ${v.views || '[X,000]'}
Brand to contact: ${v.brand || '[Brand Name]'}
Sponsor category: ${TYPES.find(t => t.id === type)?.label}

Channel niche: cinematic AI-rendered automotive content — dark luxury aesthetic, high-CPM audience of car enthusiasts, investors, and entrepreneurs aged 22–45.

Email must include:
- Subject line (compelling, specific, under 60 chars)
- Personalised opener referencing their brand specifically
- Channel value proposition in 2 sentences
- Audience fit statement
- Specific ask (15-min call or email reply)
- Confident professional sign-off

Under 180 words total. No desperation. Write as an equal, not a fan.`}
      />
    </div>
  )
}
