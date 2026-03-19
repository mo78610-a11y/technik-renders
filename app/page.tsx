'use client'
import dynamic from 'next/dynamic'

export const runtime = 'edge'

const Shell = dynamic(() => import('./components/Shell'), { ssr: false })

export default function Home() {
  return <Shell />
}
