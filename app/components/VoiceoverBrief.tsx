'use client'
import AIModule from './AIModule'

export default function VoiceoverBrief() {
  return (
    <AIModule
      title="Voiceover Brief"
      subtitle="ElevenLabs settings + voice direction for every video. Paste directly into your workflow."
      outputLabel="Generate Brief"
      fields={[
        { id: 'title',  placeholder: 'Video title',                                                          flex: 3 },
        { id: 'tone',   placeholder: 'Tone', default: 'dark, cinematic, authoritative luxury narrator',       flex: 2 },
        { id: 'voice',  placeholder: 'ElevenLabs voice name (or leave blank for recommendation)',             flex: 2 },
      ]}
      system={`You are a voice director for "Technik Renders" — a cinematic automotive YouTube channel. You produce precise ElevenLabs setup briefs that ensure every video has a consistent, premium audio identity. The channel's voice is calm, deep, authoritative — like a luxury car documentary narrator. Female AI voices preferred for distinctiveness.`}
      promptFn={v => `Generate a complete ElevenLabs voiceover brief for:

Video: "${v.title}"
Desired tone: ${v.tone}
Preferred voice: ${v.voice || 'recommend best match'}

Brief must include:

RECOMMENDED VOICE
[Voice name + why it fits this video's tone]

ELEVENLABS SETTINGS
- Stability: [value 0–100]
- Similarity Boost: [value 0–100]
- Style Exaggeration: [value 0–100]
- Speaker Boost: [yes/no]

DELIVERY NOTES
[5 bullet points on pacing, emphasis, pauses, and emotion for this specific script]

PACING GUIDE
[How fast/slow different sections should feel — hook vs body vs CTA vs close]

QUALITY CHECK
[3 things to listen for before approving the final render]

EXPORT SETTINGS
Format: MP3 · 192kbps · 44.1kHz stereo`}
    />
  )
}
