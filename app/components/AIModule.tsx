'use client'
import { useState } from 'react'

export async function streamClaude(
  system: string,
  user: string,
  onChunk: (t: string) => void
): Promise<string> {
  const r = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ system, user })
  })
  const reader = r.body!.getReader()
  const dec = new TextDecoder()
  let full = ''
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    dec.decode(value).split('\n').filter(l => l.startsWith('data: ')).forEach(line => {
      try {
        const d = JSON.parse(line.slice(6))
        if (d.type === 'content_block_delta' && d.delta?.text) {
          full += d.delta.text
          onChunk(full)
        }
      } catch {}
    })
  }
  return full
}

interface Field {
  id: string
  placeholder: string
  default?: string
  flex?: number
  type?: 'input' | 'select'
  options?: string[]
}

interface AIModuleProps {
  title: string
  subtitle: string
  fields: Field[]
  system: string
  promptFn: (vals: Record<string, string>) => string
  outputLabel?: string
}

export default function AIModule({ title, subtitle, fields, system, promptFn, outputLabel }: AIModuleProps) {
  const init = Object.fromEntries(fields.map(f => [f.id, f.default || '']))
  const [vals, setVals] = useState<Record<string, string>>(init)
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  async function generate() {
    if (loading) return
    setLoading(true)
    setOutput('')
    await streamClaude(system, promptFn(vals), txt => setOutput(txt))
    setLoading(false)
  }

  function copy() {
    navigator.clipboard.writeText(output)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <div>
      <h1 className="page-title">{title}</h1>
      <p className="page-sub">{subtitle}</p>

      <div className="input-row">
        {fields.map(f => (
          f.type === 'select' ? (
            <select
              key={f.id}
              className="input"
              style={{ flex: f.flex ?? 1, minWidth: 160 }}
              value={vals[f.id]}
              onChange={e => setVals(v => ({ ...v, [f.id]: e.target.value }))}
            >
              {f.options?.map(o => <option key={o} value={o}>{o}</option>)}
            </select>
          ) : (
            <input
              key={f.id}
              className="input"
              style={{ flex: f.flex ?? 1, minWidth: 180 }}
              placeholder={f.placeholder}
              value={vals[f.id]}
              onChange={e => setVals(v => ({ ...v, [f.id]: e.target.value }))}
            />
          )
        ))}
        <button
          className="btn btn-primary"
          onClick={generate}
          disabled={loading}
        >
          {loading ? (
            <><span className="spinner" /> Generating...</>
          ) : (
            outputLabel || 'Generate'
          )}
        </button>
      </div>

      {output ? (
        <div>
          <div className="output-box">{output}</div>
          <div className="copy-row">
            <button className="copy-btn" onClick={copy}>
              {copied ? 'Copied ✓' : 'Copy to clipboard'}
            </button>
          </div>
        </div>
      ) : (
        <div className="card-ghost">
          {loading ? 'AI is writing...' : 'Output will appear here.'}
        </div>
      )}
    </div>
  )
}
