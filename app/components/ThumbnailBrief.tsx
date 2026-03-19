'use client'
import AIModule from './AIModule'

export default function ThumbnailBrief() {
  return (
    <AIModule
      title="Thumbnail Brief"
      subtitle="Midjourney prompts + Canva layout instructions. Generates 3 A/B variants per video."
      outputLabel="Generate Brief"
      fields={[
        { id: 'title',    placeholder: 'Video title',                                        flex: 3 },
        { id: 'car',      placeholder: 'Featured car (e.g. Porsche 911, Lamborghini Urus)',  flex: 2 },
        { id: 'mood',     placeholder: 'Mood / colour palette',  default: 'dark noir gold',  flex: 2 },
      ]}
      system={`You are a creative director for "Technik Renders" — a cinematic YouTube channel with a dark luxury automotive aesthetic, similar to high-end car design accounts like Avante Designs. You produce thumbnail briefs that are visually striking, high-CTR, and consistent with a premium editorial brand.

Thumbnail style:
- Dark studio or night-city backgrounds
- Car as hero — sharp, clean, photorealistic render quality
- Gold or white bold text overlays
- Minimal text — 3–5 words max
- Aspect ratio: 1280×720px

Output is a brief for both Midjourney (image generation) and Canva (text overlay).`}
      promptFn={v => `Create 3 thumbnail variants for:
Video: "${v.title}"
Car: ${v.car || 'luxury sports car'}
Mood: ${v.mood}

For each variant provide:

VARIANT [N] — [label e.g. "Dark Studio", "Motion Blur", "Detail Close-up"]

MIDJOURNEY PROMPT:
[Full Midjourney prompt — cinematic, photorealistic, 8K, editorial. Include lighting, angle, background, mood. End with: --ar 16:9 --style raw --q 2]

CANVA OVERLAY:
- Text: [3–5 words]
- Font: Bebas Neue or Montserrat Black
- Size: 80–100px
- Colour: [Gold #C9A84C or White]
- Position: [Bottom-left / Centre / Top]
- Drop shadow: yes, 40% opacity black

CTR REASON: [One sentence — why this thumbnail makes someone click]

---`}
    />
  )
}
