'use client'

const CAL = [
  { d:1,  t:'Top 10 Most Insane Supercars Ever Rendered',                    f:'Listicle',    r:'AdSense',          car:'Multi' },
  { d:2,  t:'Why Billionaires Obsess Over Paint Protection Film',             f:'Explainer',   r:'Affiliate',        car:'Porsche 911' },
  { d:3,  t:'Porsche vs Ferrari — The Design War Nobody Talks About',         f:'Comparison',  r:'AdSense',          car:'911 vs F8' },
  { d:4,  t:"This $500K Car's Paint Job Cost More Than Most Houses",          f:'Exposé',      r:'AdSense + Prod',   car:'Bugatti' },
  { d:5,  t:'I Rendered Every Lamborghini Ever Made — Here Is the Best',      f:'Story',       r:'Sponsor',          car:'Lambo lineup' },
  { d:6,  t:'The AI Render That Broke the Internet — How It Was Made',        f:'Behind Scenes',r:'Course',          car:'Custom' },
  { d:7,  t:'Faceless Car Channels Making $1M/Year — The Full Blueprint',     f:'Trend',       r:'AdSense + Course', car:'Mixed' },
  { d:8,  t:'Is Ceramic Coating Worth It in 2025? The Real Answer',           f:'Explainer',   r:'Affiliate',        car:'BMW M4' },
  { d:9,  t:'How Billionaires Actually Maintain Their Cars',                  f:'Luxury',      r:'AdSense + Sponsor',car:'Rolls-Royce' },
  { d:10, t:'The Rarest Production Cars Ever Built — Ranked',                 f:'Listicle',    r:'AdSense',          car:'Rare roster' },
  { d:11, t:'PPF vs Vinyl Wrap — Which One Actually Wins?',                   f:'Comparison',  r:'Affiliate',        car:'GT3 RS' },
  { d:12, t:"The World's Most Expensive Car Transformations",                 f:'Showcase',    r:'AdSense + Brand',  car:'Custom builds' },
  { d:13, t:'I Spent $250,000 on This Car Render Series — Worth It?',         f:'Story',       r:'Sponsor',          car:'1-of-1 custom' },
  { d:14, t:'How to Invest $100k in a Car Business in 2025',                  f:'Finance',     r:'High CPM',         car:'Mixed fleet' },
  { d:15, t:'Top 5 Car Insurance Mistakes That Cost You Thousands',           f:'Finance',     r:'High CPM AdSense', car:'Lifestyle' },
  { d:16, t:"Scratch & Dent Insurance — What They Don't Tell You",            f:'Explainer',   r:'Product Promo',    car:'Daily driver' },
  { d:17, t:'I Tested Every Major Car Protection Product — Results',          f:'Review',      r:'Amazon Affiliate', car:'Multi' },
  { d:18, t:'Why Every Luxury Car Owner Needs PPF in 2025',                   f:'Explainer',   r:'Affiliate',        car:'Lamborghini' },
  { d:19, t:'Lamborghini vs Rolls-Royce — Which is Harder to Own?',           f:'Luxury',      r:'AdSense',          car:'Both' },
  { d:20, t:'The Complete Supercar Protection Guide for New Owners',           f:'Tutorial',    r:'Digital Product',  car:'911' },
  { d:21, t:'Building a 7-Figure Car Content Business in 2025',               f:'Brand Story', r:'Brand + Course',   car:'Brand identity' },
  { d:22, t:'The Best Dashcams for Supercars — 2025 Ranking',                 f:'Review',      r:'Amazon Affiliate', car:'GT cars' },
  { d:23, t:'This Car Design Was Rejected — Then It Sold for $10M',           f:'Story',       r:'AdSense',          car:'Concept car' },
  { d:24, t:'How AI Is Designing the Cars of 2030',                           f:'Trend',       r:'AdSense + Course', car:'Future renders' },
  { d:25, t:'The Most Stolen Luxury Cars — And How to Protect Yours',         f:'Localised',   r:'AdSense + Security',car:'AMG' },
  { d:26, t:'Rich vs Wealthy — How They Think About Cars Differently',        f:'Psychology',  r:'AdSense',          car:'Contrast shots' },
  { d:27, t:'The Car That Inspired Every Supercar After It',                  f:'History',     r:'AdSense',          car:'Miura' },
  { d:28, t:'Everything I Wish I Knew Before Starting a Car Channel',         f:'Value',       r:'Digital Product',  car:'Mixed' },
  { d:29, t:'The Most Jaw-Dropping Custom Renders of 2025',                   f:'Compilation', r:'AdSense',          car:'Custom series' },
  { d:30, t:'Month 1 of Technik Renders — What Worked, What is Next',         f:'Update',      r:'Community + Course',car:'Channel brand' },
]

const WEEKS = [
  { label: 'Week 1 — Hook & establish', days: CAL.slice(0, 7)  },
  { label: 'Week 2 — Build authority',  days: CAL.slice(7, 14) },
  { label: 'Week 3 — Monetise hard',    days: CAL.slice(14, 21)},
  { label: 'Week 4 — Scale & brand',    days: CAL.slice(21, 30)},
]

function revenueTag(r: string) {
  if (r.includes('Sponsor'))                     return 'blue'
  if (r.includes('Affiliate') || r.includes('Amazon')) return 'green'
  if (r.includes('Product') || r.includes('Course'))   return 'gold'
  if (r.includes('High CPM'))                    return 'red'
  return 'gray'
}

export default function Calendar() {
  return (
    <div>
      <h1 className="page-title">30-Day Content Calendar</h1>
      <p className="page-sub">One cinematic automotive video per day. Every video mapped to a monetisation stream. Built for Technik Renders.</p>

      {WEEKS.map(w => (
        <div className="section-block" key={w.label}>
          <p className="eyebrow gold">{w.label}</p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
            {w.days.map(d => (
              <div className="cal-row" key={d.d}>
                <span className="cal-day">D{d.d}</span>
                <span style={{ flex: 1, fontSize: 13 }}>{d.t}</span>
                <span className="tag tag-gray" style={{ fontSize: 10 }}>{d.car}</span>
                <span className="tag tag-gray" style={{ fontSize: 10 }}>{d.f}</span>
                <span className={`tag tag-${revenueTag(d.r)}`} style={{ fontSize: 10 }}>{d.r}</span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  )
}
