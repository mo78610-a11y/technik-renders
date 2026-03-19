'use client'
import { useState } from 'react'

const STEPS = [
  {
    time: '5 min',
    title: 'Topic selection',
    tool: 'Idea Engine + VidIQ',
    desc: `Open the Idea Engine tab. Select your niche. Generate 10 ideas. Pick the strongest title — the one you'd click yourself. Cross-check it in VidIQ. Only proceed if the search volume score is above 50. If nothing clears 50, regenerate with a different angle.`,
    tools: ['Claude AI', 'VidIQ'],
  },
  {
    time: '10 min',
    title: 'Script writing',
    tool: 'Script Writer',
    desc: `Open the Script Writer tab. Enter your title, tone, and CTA. Click Write Script. Copy the full output into a Google Doc titled with the video name and today's date. Read only the HOOK section — if the first 3 lines grip you, the script is ready. If not, regenerate with a stronger hook angle.`,
    tools: ['Claude AI', 'Google Docs'],
  },
  {
    time: '5 min',
    title: 'Voiceover brief',
    tool: 'Voiceover Brief',
    desc: `Open the Voiceover Brief tab. Enter your video title. Copy the ElevenLabs settings output. Go to elevenlabs.io → Speech Synthesis. Select your saved Technik Renders voice. Apply the exact stability and similarity settings from the brief. Paste the full script. Generate. Download MP3 at 192kbps.`,
    tools: ['ElevenLabs', 'Voiceover Brief tab'],
  },
  {
    time: '15 min',
    title: 'Render generation',
    tool: 'Midjourney + Higgsfield',
    desc: `Open the Thumbnail Brief tab. Copy the 3 Midjourney prompts. Run each in Midjourney. Save the best result per variant. For video B-roll: use Higgsfield with the same cinematic prompts — generate 4–6 short clips (3–5 sec each) as your render footage. These replace traditional B-roll entirely.`,
    tools: ['Midjourney', 'Higgsfield', 'Thumbnail Brief tab'],
  },
  {
    time: '10 min',
    title: 'Video assembly',
    tool: 'Invideo AI',
    desc: `Go to invideo.io → AI Video → YouTube. Paste your script. Upload your ElevenLabs MP3 as custom audio. Select Cinematic style. Auto captions ON. Replace default B-roll with your Higgsfield render clips — drag them into the timeline in order. Review auto-transitions. Export at 1080p minimum.`,
    tools: ['Invideo AI', 'Higgsfield clips'],
  },
  {
    time: '10 min',
    title: 'Thumbnail creation',
    tool: 'Canva + Midjourney',
    desc: `Take your best Midjourney render from Step 4. Import into Canva at 1280×720px. Add your bold 5-word overlay text (from the Thumbnail Brief). Font: Bebas Neue or Montserrat Black. Colour: Gold #C9A84C or white. Drop shadow: 40% black. Export both variants A and B. Upload A to YouTube, activate TubeBuddy A/B test.`,
    tools: ['Canva', 'TubeBuddy'],
  },
  {
    time: '10 min',
    title: 'SEO metadata',
    tool: 'SEO Builder + VidIQ',
    desc: `Open the SEO Builder tab. Enter your title. Copy the full package — SEO title, 230-word description, 18 tags, chapters, thumbnail text, hashtags. Verify the top 3 tags in VidIQ — confirm search volume is present. Paste everything into a Google Doc alongside the script. This is your upload-ready file.`,
    tools: ['SEO Builder tab', 'VidIQ', 'Google Docs'],
  },
  {
    time: '5 min',
    title: 'Upload & schedule',
    tool: 'YouTube Studio',
    desc: `Upload your video file. Upload thumbnail A. Paste SEO title, description (with affiliate links filled in), tags, chapters. Set end screen: promote last video + subscribe button. Add cards at 20% and 70% mark. Schedule for 8:00 AM your local time — peak automotive audience window. Monetisation: ON. All ad types enabled.`,
    tools: ['YouTube Studio'],
  },
  {
    time: '0 min',
    title: 'Auto-distribution',
    tool: 'Zapier (runs itself)',
    desc: `One-time setup only: Zapier trigger on new YouTube upload → auto-clips and posts to Instagram Reels, TikTok, and X with a pre-set caption template. Once activated, this step runs forever with zero input. Every upload is automatically distributed across 4 platforms simultaneously.`,
    tools: ['Zapier'],
  },
  {
    time: '20 min',
    title: 'Weekly review (Sunday)',
    tool: 'YouTube Analytics',
    desc: `Every Sunday: check YouTube Studio analytics. Kill any video under 35% avg view duration after 7 days — study why the hook failed. Identify your top performer — create a follow-up on the same topic. Update any broken affiliate links. Send one sponsor outreach email using the Outreach tab. Review Zapier automation logs.`,
    tools: ['YouTube Studio', 'Outreach tab'],
  },
]

function Tag({ text, type = 'gray' }: { text: string; type?: string }) {
  return <span className={`tag tag-${type}`}>{text}</span>
}

export default function SOP() {
  const [open, setOpen] = useState<number | null>(null)

  const totalTime = '65 min/day'

  return (
    <div>
      <h1 className="page-title">Daily SOP</h1>
      <p className="page-sub">
        Standard operating procedure for Technik Renders. Run this every day.
        Click any step to expand the full instructions.
      </p>

      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 28 }}>
        <Tag text={`Total: ~${totalTime}`} type="gold" />
        <Tag text="Zero recording"        type="green" />
        <Tag text="Zero editing"          type="green" />
        <Tag text="Zero face time"        type="green" />
        <Tag text="AI does the work"      type="blue" />
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {STEPS.map((s, i) => (
          <div
            key={i}
            className={`sop-item ${open === i ? 'open' : ''}`}
          >
            <button
              className="sop-trigger"
              onClick={() => setOpen(open === i ? null : i)}
            >
              <span style={{
                fontFamily: 'var(--font-mono)',
                fontSize: 11,
                color: 'var(--gold)',
                minWidth: 44,
              }}>
                {s.time}
              </span>
              <span style={{ flex: 1, fontSize: 13, fontWeight: 600 }}>
                {s.title}
              </span>
              <Tag text={s.tool} type="gray" />
              <span style={{ color: 'var(--text3)', fontSize: 11, marginLeft: 8 }}>
                {open === i ? '▲' : '▼'}
              </span>
            </button>

            {open === i && (
              <div className="sop-body">
                <p style={{ marginBottom: 12 }}>{s.desc}</p>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  {s.tools.map(t => (
                    <Tag key={t} text={t} type="blue" />
                  ))}
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
