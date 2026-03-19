'use client'
import AIModule from './AIModule'

const NICHES = ['Luxury automotive', 'Car renders & design', 'PPF & car protection', 'Supercar lifestyle', 'Automotive investment', 'Car modification', 'EV & future cars', 'Detailing & care']

export default function IdeaEngine() {
  return (
    <AIModule
      title="Idea Engine"
      subtitle="Generate viral video ideas for Technik Renders. High-CPM, curiosity-driven, render-focused."
      outputLabel="Generate Ideas"
      fields={[
        {
          id: 'niche',
          placeholder: 'Select niche',
          default: 'Luxury automotive',
          flex: 2,
          type: 'select',
          options: NICHES,
        },
        {
          id: 'count',
          placeholder: 'How many?',
          default: '10',
          flex: 1,
          type: 'select',
          options: ['5', '10', '15', '20'],
        },
        {
          id: 'tone',
          placeholder: 'Angle (e.g. dark luxury, aspirational, exposé)',
          default: 'cinematic dark luxury',
          flex: 2,
        },
      ]}
      system={`You are a YouTube strategist for a faceless cinematic automotive channel called "Technik Renders". The channel produces AI-generated render videos — dark, luxury, editorial aesthetic similar to high-end car design accounts. Target audience: car enthusiasts, investors, entrepreneurs aged 22–45. High-CPM niche.

Format output as a clean numbered list. Each idea:
Line 1: VIDEO TITLE (punchy, curiosity-driven, under 70 chars)
Line 2: Hook angle (one sentence — what makes this irresistible to click)
Line 3: Render style (e.g. "Dark studio render, neon accents, slow rotation")
Blank line between ideas. No preamble.`}
      promptFn={v => `Generate ${v.count} viral YouTube video ideas for the "${v.niche}" niche. Tone/angle: ${v.tone}. Each idea must trigger curiosity, target high-CPM viewers, be searchable on YouTube, and work as a cinematic 8–12 minute video using AI renders. Include hook angle and render style for each.`}
    />
  )
}
