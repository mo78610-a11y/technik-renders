'use client'
import AIModule from './AIModule'

export default function SEOBuilder() {
  return (
    <AIModule
      title="SEO Builder"
      subtitle="Title · Description · Tags · Chapters · Thumbnail text. Paste-ready for YouTube Studio."
      outputLabel="Build SEO Package"
      fields={[
        { id: 'title',    placeholder: 'Video title or topic',                          flex: 3 },
        { id: 'keywords', placeholder: 'Target keywords (optional)',                    flex: 2 },
        { id: 'link1',    placeholder: 'Affiliate link label (e.g. PPF Guide)',         flex: 2 },
      ]}
      system={`You are a YouTube SEO specialist for a cinematic automotive channel called "Technik Renders". Produce metadata that ranks, converts, and targets high-CPM automotive audiences. Be specific. Use real keyword structures people search.`}
      promptFn={v => `Produce a full YouTube SEO package for:
Video title: "${v.title}"
Target keywords: ${v.keywords || 'auto-determine from title'}
Affiliate product: ${v.link1 || 'car protection guide'}

Format EXACTLY as follows:

SEO TITLE
[Under 70 characters. Keyword-first. Curiosity-driven. Do not repeat the raw title exactly.]

DESCRIPTION
[230 words. First sentence contains primary keyword naturally. Include 3 keyword variations. Add [${v.link1 || 'AFFILIATE LINK'}] as placeholder. Include timestamps placeholder [CHAPTERS BELOW]. End with: "Subscribe for weekly cinematic automotive content — Technik Renders."]

TAGS
[18 tags, comma-separated, ranked by search relevance]

CHAPTERS
[7 chapters starting at 0:00. Realistic durations for a 10-minute video.]

THUMBNAIL TEXT
[5 bold words maximum for text overlay — punchy, high contrast]

HASHTAGS
[5 hashtags for description footer]`}
    />
  )
}
