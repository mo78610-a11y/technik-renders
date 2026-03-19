'use client'
import AIModule from './AIModule'

export default function ScriptWriter() {
  return (
    <AIModule
      title="Script Writer"
      subtitle="Full 10-minute cinematic voiceover scripts. Paste straight into ElevenLabs."
      outputLabel="Write Script"
      fields={[
        { id: 'title',    placeholder: 'Video title',                                                              flex: 3 },
        { id: 'tone',     placeholder: 'Narrator tone',         default: 'dark luxury narrator — deep, calm, cinematic',  flex: 2 },
        { id: 'cta',      placeholder: 'Mid-roll CTA',          default: 'check the description for links mentioned',     flex: 2 },
        { id: 'product',  placeholder: 'Affiliate/product plug', default: 'PPF protection guide — link in description',    flex: 2 },
      ]}
      system={`You are an elite YouTube scriptwriter for "Technik Renders" — a faceless cinematic automotive channel. You write pure voiceover scripts only. No stage directions. No timestamps. No camera notes. Structure with ALL-CAPS section headers.

Style: editorial, authoritative, cinematic. Like a luxury car documentary narrator. High information density. Zero filler. Every sentence earns its place. Viewers must feel they are watching something premium.

The channel uses AI-generated car renders — dark studio lighting, editorial angles, slow rotations. Scripts must complement this visual style.`}
      promptFn={v => `Write a full 10-minute YouTube voiceover script for Technik Renders.

Title: "${v.title}"
Narrator tone: ${v.tone}

Structure:
HOOK — 30-second cold open. Start with a bold statement, provocative question, or shocking fact. Do NOT introduce the channel. Grab immediately.
SECTION 1 — [topic section]
SECTION 2 — [topic section]
SECTION 3 — [topic section]
SECTION 4 — [topic section]
SECTION 5 — [topic section]
MID-ROLL CTA — Natural 15-second integration: "${v.cta}" — mention: ${v.product}
CLOSE — One powerful, memorable final line that makes viewers want to subscribe and return.

Pure voiceover only. No directions. No timestamps.`}
    />
  )
}
