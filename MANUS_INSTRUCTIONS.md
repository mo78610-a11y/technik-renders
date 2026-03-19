# MANUS AUTONOMOUS TASK — TECHNIK RENDERS YOUTUBE SYSTEM

## YOUR JOB
You are building and deploying a complete YouTube content creation system for a luxury automotive channel called "Technik Renders". Execute every step below autonomously from start to finish. Do not stop or ask for confirmation unless a credential is missing.

---

## STEP 1 — CREATE PROJECT STRUCTURE

Run these commands:

```bash
mkdir -p technik-renders
cd technik-renders
mkdir -p app/components app/api/generate public
```

---

## STEP 2 — CREATE ALL FILES

Create every file listed below with the exact contents provided in the FILES section of this document.

File list:
- package.json
- next.config.js
- vercel.json
- .env.local  (you will fill ANTHROPIC_API_KEY)
- app/layout.tsx
- app/globals.css
- app/page.tsx
- app/components/Shell.tsx
- app/components/Dashboard.tsx
- app/components/IdeaEngine.tsx
- app/components/ScriptWriter.tsx
- app/components/SEOBuilder.tsx
- app/components/ThumbnailBrief.tsx
- app/components/Calendar.tsx
- app/components/SOP.tsx
- app/components/Outreach.tsx
- app/components/VoiceoverBrief.tsx

---

## STEP 3 — INSTALL & BUILD

```bash
npm install
npm run build
```

---

## STEP 4 — DEPLOY TO VERCEL

```bash
npx vercel deploy --prod --scope=mohamed-yaseens-projects-c5bb4704
```

When prompted for a token use the Vercel token from the user.
Project name: technik-renders
Framework: Next.js

---

## STEP 5 — SEND LIVE URL TO EMAIL

After successful deployment, send the live URL to: logivo92@gmail.com
Subject: "Technik Renders — YT Control Center is Live"

---

## SUCCESS CRITERIA
- All files created with zero errors
- `npm run build` passes clean
- Vercel deployment returns a live URL
- Email sent to logivo92@gmail.com with the URL
