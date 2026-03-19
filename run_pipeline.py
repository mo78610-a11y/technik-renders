#!/usr/bin/env python3
"""
TECHNIK RENDERS — FULL AUTONOMOUS PIPELINE
Updated AI Stack:
  1. Prompt development    → Claude
  2. Image creation        → NanoBanana Pro & 2
  3. Cinematic video       → Kling 3.0 + Grok + Higgsfield Cinema Studio
  4. Editing & refinement  → Weavy
Run: python3 run_pipeline.py
"""

import os, sys, json, datetime, subprocess, traceback

LOG_FILE = "technik-pipeline/logs/run.log"
RESULTS  = {}

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs("technik-pipeline/logs", exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def run_step(name, fn):
    log(f"▶ STARTING: {name}")
    try:
        result = fn()
        RESULTS[name] = "✓ Complete"
        log(f"✓ DONE: {name}")
        return result
    except Exception as e:
        RESULTS[name] = f"✗ Failed: {str(e)}"
        log(f"✗ FAILED: {name} — {str(e)}")
        traceback.print_exc()
        return None

def setup():
    dirs = [
        "technik-pipeline/output/scripts",
        "technik-pipeline/output/audio",
        "technik-pipeline/output/images",
        "technik-pipeline/output/renders",
        "technik-pipeline/output/thumbnails",
        "technik-pipeline/output/videos",
        "technik-pipeline/output/seo",
        "technik-pipeline/output/social",
        "technik-pipeline/logs",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    log("Pipeline initialized — Technik Renders AI Stack v2")
    log("Stack: Claude → NanoBanana → Kling 3.0 + Grok + Higgsfield → Weavy")

# ── PHASE 1: IDEA (Claude) ───────────────────────────────────
def generate_idea():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    system = (
        "You are a YouTube strategist for Technik Renders — a faceless cinematic automotive channel. "
        "Generate high-CPM viral video ideas for luxury car audiences aged 22-45. "
        "Output ONLY valid JSON. No markdown. No explanation."
    )
    prompt = (
        'Generate today\'s best YouTube video idea for Technik Renders. '
        'Return JSON exactly: {'
        '"title": "video title under 70 chars", '
        '"hook": "one sentence hook", '
        '"angle": "unique editorial angle", '
        '"featured_car": "hero car for renders", '
        '"render_style": "dark studio cinematic — describe lighting mood colour", '
        '"nanobana_style": "NanoBanana image generation style descriptor", '
        '"kling_motion": "camera movement for Kling 3.0 — e.g. slow dolly in, orbit, pull back", '
        '"revenue_type": "AdSense|Affiliate|Sponsor|Product", '
        '"affiliate_product": "relevant product to promote", '
        '"target_keywords": ["kw1","kw2","kw3"], '
        '"estimated_cpm": "$8-15"}'
    )
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=600,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    idea = json.loads(msg.content[0].text)
    idea["date"] = datetime.date.today().isoformat()
    with open("technik-pipeline/output/idea.json", "w") as f:
        json.dump(idea, f, indent=2)
    log(f"Idea: {idea['title']}")
    log(f"Car: {idea['featured_car']} | Revenue: {idea['revenue_type']}")
    return idea

# ── PHASE 2: SCRIPT (Claude) ─────────────────────────────────
def write_script():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    with open("technik-pipeline/output/idea.json") as f:
        idea = json.load(f)
    system = (
        "You are an elite YouTube scriptwriter for Technik Renders — a faceless cinematic "
        "automotive channel with dark luxury editorial aesthetics. "
        "Write pure voiceover scripts only. No stage directions. No timestamps. "
        "Use ALL-CAPS section headers. High density, zero filler. "
        "Tone: deep luxury documentary narrator — calm, authoritative, cinematic."
    )
    prompt = f"""Write a full 10-minute YouTube voiceover script.
Title: "{idea['title']}"
Car: {idea['featured_car']}
Angle: {idea['angle']}
Promote: {idea['affiliate_product']}

HOOK
[30-second cold open — bold statement or shocking fact. No channel intro. Grip immediately.]

SECTION 1
SECTION 2
SECTION 3
SECTION 4
SECTION 5

MID-ROLL CTA
[15 sec — natural mention of {idea['affiliate_product']} — link in description.]

CLOSE
[One powerful final line that makes viewers subscribe.]

Pure voiceover only. No directions."""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    script = msg.content[0].text
    slug = idea['title'].lower().replace(' ','_').replace("'","")[:50]
    path = f"technik-pipeline/output/scripts/script_{slug}.txt"
    with open(path, "w") as f:
        f.write(f"TITLE: {idea['title']}\nDATE: {idea['date']}\n{'='*60}\n\n{script}")
    with open("technik-pipeline/output/script_path.txt", "w") as f:
        f.write(path)
    log(f"Script: {len(script)} chars → {path}")
    return script

# ── PHASE 3: VOICEOVER (ElevenLabs) ─────────────────────────
def generate_voiceover():
    import requests
    key      = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
    with open("technik-pipeline/output/script_path.txt") as f:
        path = f.read().strip()
    with open(path) as f:
        raw = f.read()
    script = raw.split("="*60)[-1].strip()
    r = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        json={"text": script, "model_id": "eleven_multilingual_v2",
              "voice_settings": {"stability": 0.55, "similarity_boost": 0.75,
                                 "style": 0.0, "use_speaker_boost": True}}
    )
    if r.status_code == 200:
        out = "technik-pipeline/output/audio/voiceover.mp3"
        with open(out, "wb") as f:
            f.write(r.content)
        log(f"Voiceover saved: {out}")
    else:
        raise Exception(f"ElevenLabs {r.status_code}: {r.text}")

# ── PHASE 4: IMAGE & VIDEO BRIEFS (Claude → NanoBanana + Kling + Grok + Higgsfield + Weavy) ──
def generate_creative_briefs():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    with open("technik-pipeline/output/idea.json") as f:
        idea = json.load(f)

    system = (
        "You are a creative director for Technik Renders. "
        "The production stack is: NanoBanana Pro & 2 for images, "
        "Kling 3.0 + Grok + Higgsfield Cinema Studio for video, Weavy for editing. "
        "Output ONLY valid JSON. No markdown."
    )
    prompt = f"""Generate complete creative production briefs for:
Video: "{idea['title']}"
Car: {idea['featured_car']}
Render style: {idea['render_style']}
NanoBanana style: {idea['nanobana_style']}
Kling motion: {idea['kling_motion']}

Return JSON:
{{
  "nanobanana_image_prompts": [
    {{
      "id": "img_01",
      "use": "hero render — main thumbnail base",
      "prompt": "full NanoBanana Pro prompt — photorealistic, 8K, cinematic",
      "settings": {{"style": "photorealistic", "ar": "16:9", "quality": "ultra"}}
    }},
    {{
      "id": "img_02",
      "use": "b-roll still 1",
      "prompt": "full NanoBanana prompt",
      "settings": {{"style": "cinematic", "ar": "16:9", "quality": "ultra"}}
    }},
    {{
      "id": "img_03",
      "use": "b-roll still 2 — detail shot",
      "prompt": "full NanoBanana prompt",
      "settings": {{"style": "editorial", "ar": "16:9", "quality": "ultra"}}
    }},
    {{
      "id": "img_04",
      "use": "b-roll still 3 — lifestyle/environment",
      "prompt": "full NanoBanana prompt",
      "settings": {{"style": "luxury", "ar": "16:9", "quality": "ultra"}}
    }},
    {{
      "id": "img_05",
      "use": "thumbnail variant A — dark studio",
      "prompt": "full NanoBanana prompt for thumbnail",
      "settings": {{"style": "photorealistic", "ar": "16:9", "quality": "ultra"}}
    }},
    {{
      "id": "img_06",
      "use": "thumbnail variant B — motion/action",
      "prompt": "full NanoBanana prompt for thumbnail",
      "settings": {{"style": "cinematic", "ar": "16:9", "quality": "ultra"}}
    }}
  ],
  "kling_video_prompts": [
    {{
      "id": "clip_01",
      "source_image": "img_01",
      "duration": "5s",
      "motion": "slow cinematic dolly in",
      "prompt": "full Kling 3.0 prompt — cinematic motion from img_01",
      "camera": "dolly in, slight pan right",
      "mood": "dark luxury"
    }},
    {{
      "id": "clip_02",
      "source_image": "img_02",
      "duration": "4s",
      "motion": "orbital reveal",
      "prompt": "full Kling 3.0 prompt",
      "camera": "slow orbit left to right",
      "mood": "editorial"
    }},
    {{
      "id": "clip_03",
      "source_image": "img_03",
      "duration": "3s",
      "motion": "pull back reveal",
      "prompt": "full Kling 3.0 prompt",
      "camera": "smooth pull back",
      "mood": "cinematic"
    }},
    {{
      "id": "clip_04",
      "source_image": "img_04",
      "duration": "4s",
      "motion": "hero shot pan",
      "prompt": "full Kling 3.0 prompt",
      "camera": "slow pan with depth",
      "mood": "luxury"
    }}
  ],
  "grok_enhancement_prompt": "Grok image enhancement prompt — describe how to upscale and enhance the NanoBanana images before passing to Kling",
  "higgsfield_hero_prompt": "Higgsfield Cinema Studio prompt for the 8-10 second hero opening sequence — cinematic, dark luxury automotive",
  "weavy_edit_sequence": [
    "Step 1: Import all Kling clips into Weavy node editor",
    "Step 2: Node sequence — hero_clip → b_roll_01 → b_roll_02 → b_roll_03 → b_roll_04",
    "Step 3: Apply LUT: Dark Luxury Cinematic",
    "Step 4: Add voiceover.mp3 as audio track — sync to cuts",
    "Step 5: Auto-caption layer — white text, bottom centre, Syne Bold font",
    "Step 6: Colour grade — crush blacks, boost gold/amber tones",
    "Step 7: Export — 1080p MP4, H.264, 192kbps audio"
  ],
  "thumbnail_canva_instructions": [
    {{
      "variant": "A",
      "source_image": "img_05",
      "overlay_text": "5 bold words max",
      "font": "Bebas Neue",
      "font_size": "100px",
      "colour": "#C9A84C",
      "position": "bottom-left",
      "effects": "drop shadow 40% black"
    }},
    {{
      "variant": "B",
      "source_image": "img_06",
      "overlay_text": "5 bold words max",
      "font": "Montserrat Black",
      "font_size": "90px",
      "colour": "#FFFFFF",
      "position": "centre",
      "effects": "drop shadow 60% black"
    }}
  ]
}}"""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    briefs = json.loads(msg.content[0].text)
    with open("technik-pipeline/output/renders/creative_briefs.json", "w") as f:
        json.dump(briefs, f, indent=2)

    # Write human-readable production sheet
    with open("technik-pipeline/output/renders/PRODUCTION_SHEET.txt", "w") as f:
        f.write(f"{'='*60}\n")
        f.write(f"TECHNIK RENDERS — PRODUCTION SHEET\n")
        f.write(f"Video: {idea['title']}\n")
        f.write(f"Date: {idea['date']}\n")
        f.write(f"{'='*60}\n\n")

        f.write("── STEP 1: NANOBANANA IMAGE GENERATION ────────────────\n\n")
        for img in briefs["nanobana_image_prompts"]:
            f.write(f"IMAGE {img['id'].upper()} — {img['use'].upper()}\n")
            f.write(f"Prompt: {img['prompt']}\n")
            f.write(f"Settings: {json.dumps(img['settings'])}\n")
            f.write(f"Save as: {img['id']}.png\n\n")

        f.write("── STEP 2: GROK ENHANCEMENT ────────────────────────────\n\n")
        f.write(f"{briefs['grok_enhancement_prompt']}\n\n")

        f.write("── STEP 3: KLING 3.0 VIDEO GENERATION ─────────────────\n\n")
        for clip in briefs["kling_video_prompts"]:
            f.write(f"CLIP {clip['id'].upper()} — from {clip['source_image'].upper()}\n")
            f.write(f"Duration: {clip['duration']} | Motion: {clip['motion']}\n")
            f.write(f"Camera: {clip['camera']}\n")
            f.write(f"Prompt: {clip['prompt']}\n")
            f.write(f"Save as: {clip['id']}.mp4\n\n")

        f.write("── STEP 4: HIGGSFIELD CINEMA STUDIO ────────────────────\n\n")
        f.write(f"Hero sequence prompt:\n{briefs['higgsfield_hero_prompt']}\n")
        f.write(f"Save as: hero_sequence.mp4\n\n")

        f.write("── STEP 5: WEAVY NODE EDITING ──────────────────────────\n\n")
        for step in briefs["weavy_edit_sequence"]:
            f.write(f"{step}\n")
        f.write("\n")

        f.write("── STEP 6: THUMBNAIL (Canva) ───────────────────────────\n\n")
        for t in briefs["thumbnail_canva_instructions"]:
            f.write(f"VARIANT {t['variant']}:\n")
            f.write(f"Source: {t['source_image']}.png\n")
            f.write(f"Text: {t['overlay_text']}\n")
            f.write(f"Font: {t['font']} {t['font_size']} | Colour: {t['colour']}\n")
            f.write(f"Position: {t['position']} | Effects: {t['effects']}\n\n")

    log(f"Creative briefs: {len(briefs['nanobana_image_prompts'])} NanoBanana + {len(briefs['kling_video_prompts'])} Kling + Higgsfield + Weavy edit")
    return briefs

# ── PHASE 5: SEO (Claude) ────────────────────────────────────
def generate_seo():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    with open("technik-pipeline/output/idea.json") as f:
        idea = json.load(f)
    system = (
        "You are a YouTube SEO specialist for Technik Renders. "
        "Produce metadata that ranks and converts for high-CPM automotive audiences. "
        "Output ONLY valid JSON. No markdown."
    )
    prompt = f"""YouTube SEO package for:
Title: "{idea['title']}"
Car: {idea['featured_car']}
Keywords: {idea['target_keywords']}
Affiliate: {idea['affiliate_product']}

Return JSON:
{{
  "seo_title": "under 70 chars, keyword-first",
  "description": "230 words, keyword in line 1, 3 variations, [AFFILIATE LINK] placeholder, subscribe CTA",
  "tags": ["t1","t2","t3","t4","t5","t6","t7","t8","t9","t10","t11","t12","t13","t14","t15","t16","t17","t18"],
  "chapters": [{{"time":"0:00","title":"ch1"}},{{"time":"1:20","title":"ch2"}},{{"time":"2:45","title":"ch3"}},{{"time":"4:30","title":"ch4"}},{{"time":"6:15","title":"ch5"}},{{"time":"8:00","title":"ch6"}},{{"time":"9:20","title":"ch7"}}],
  "hashtags": ["#h1","#h2","#h3","#h4","#h5"],
  "thumbnail_text": "5 bold words"
}}"""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=1000, system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    seo = json.loads(msg.content[0].text)
    with open("technik-pipeline/output/seo/seo_package.json", "w") as f:
        json.dump(seo, f, indent=2)
    chapters_str = "\n".join([f"{c['time']} {c['title']}" for c in seo['chapters']])
    hashtags_str = " ".join(seo['hashtags'])
    full_desc = (seo['description'].replace("[AFFILIATE LINK]", f"→ {idea['affiliate_product']} [LINK IN DESCRIPTION]")
                 + f"\n\n— TIMESTAMPS —\n{chapters_str}\n\n{hashtags_str}")
    with open("technik-pipeline/output/seo/UPLOAD_READY.txt", "w") as f:
        f.write(f"{'='*60}\nYOUTUBE UPLOAD — PASTE READY\n{'='*60}\n\n")
        f.write(f"TITLE:\n{seo['seo_title']}\n\n")
        f.write(f"DESCRIPTION:\n{full_desc}\n\n")
        f.write(f"TAGS:\n{', '.join(seo['tags'])}\n\n")
        f.write(f"THUMBNAIL TEXT:\n{seo['thumbnail_text']}\n")
    log(f"SEO: {seo['seo_title']}")
    return seo

# ── PHASE 6: SOCIAL COPY (Claude) ───────────────────────────
def generate_social_copy():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    with open("technik-pipeline/output/idea.json") as f:
        idea = json.load(f)
    system = (
        "You are a social media strategist for Technik Renders — cinematic automotive brand. "
        "Write platform-native captions that drive YouTube clicks. Output ONLY valid JSON."
    )
    prompt = f"""Social captions for:
Title: "{idea['title']}"
Hook: "{idea['hook']}"
Car: {idea['featured_car']}

Return JSON:
{{
  "instagram_reel_caption": "under 150 chars + 5 hashtags + link in bio CTA",
  "tiktok_caption": "under 100 chars + 3 hashtags",
  "x_post": "under 240 chars with [YOUTUBE_LINK]",
  "instagram_story_text": "5 words bold overlay",
  "youtube_community_post": "under 200 chars to announce video to subscribers"
}}"""
    msg = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=500, system=system,
        messages=[{"role": "user", "content": prompt}]
    )
    social = json.loads(msg.content[0].text)
    with open("technik-pipeline/output/social/social_copy.json", "w") as f:
        json.dump(social, f, indent=2)
    with open("technik-pipeline/output/social/SOCIAL_READY.txt", "w") as f:
        f.write(f"{'='*60}\nSOCIAL MEDIA CAPTIONS — PASTE READY\n{'='*60}\n\n")
        for k, v in social.items():
            f.write(f"{k.upper().replace('_',' ')}:\n{v}\n\n")
    log("Social copy generated")
    return social

# ── PHASE 7: YOUTUBE UPLOAD ──────────────────────────────────
def upload_to_youtube():
    VIDEO_PATH = "technik-pipeline/output/videos/final_video.mp4"
    THUMB_PATH  = "technik-pipeline/output/thumbnails/thumbnail_A.jpg"
    if not os.path.exists(VIDEO_PATH):
        log("VIDEO NOT FOUND — skipping upload")
        log("Assemble in Weavy → export → place at output/videos/final_video.mp4 → re-run")
        return None
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = Credentials(
        token=None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload",
                "https://www.googleapis.com/auth/youtube"]
    )
    creds.refresh(Request())
    youtube = build("youtube", "v3", credentials=creds)
    with open("technik-pipeline/output/seo/seo_package.json") as f:
        seo = json.load(f)
    with open("technik-pipeline/output/idea.json") as f:
        idea = json.load(f)
    chapters_str = "\n".join([f"{c['time']} {c['title']}" for c in seo['chapters']])
    hashtags_str = " ".join(seo['hashtags'])
    full_desc = (seo['description'].replace("[AFFILIATE LINK]", "→ Link below")
                 + f"\n\n— TIMESTAMPS —\n{chapters_str}\n\n{hashtags_str}")
    body = {
        "snippet": {
            "title": seo["seo_title"],
            "description": full_desc,
            "tags": seo["tags"],
            "categoryId": "2",
            "defaultLanguage": "en"
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}
    }
    media = MediaFileUpload(VIDEO_PATH, chunksize=-1, resumable=True)
    req = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = None
    while response is None:
        status, response = req.next_chunk()
        if status:
            log(f"Upload: {int(status.progress()*100)}%")
    video_id  = response["id"]
    video_url = f"https://youtube.com/watch?v={video_id}"
    if os.path.exists(THUMB_PATH):
        youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(THUMB_PATH)).execute()
        log("Thumbnail set")
    with open("technik-pipeline/output/video_id.txt", "w") as f:
        f.write(video_id)
    with open("technik-pipeline/output/video_url.txt", "w") as f:
        f.write(video_url)
    log(f"YouTube live: {video_url}")
    return video_url

# ── PHASE 8: REPORT EMAIL ────────────────────────────────────
def send_report():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    with open("technik-pipeline/output/idea.json") as f:
        idea = json.load(f)
    video_url = "Not yet uploaded"
    try:
        with open("technik-pipeline/output/video_url.txt") as f:
            video_url = f.read().strip()
    except: pass
    social = {}
    try:
        with open("technik-pipeline/output/social/social_copy.json") as f:
            social = json.load(f)
    except: pass
    now = datetime.datetime.now().strftime("%d %B %Y, %H:%M")
    steps_html = "".join([
        f'<tr><td style="padding:8px;border:1px solid #eee;font-weight:600;font-size:12px">{k}</td>'
        f'<td style="padding:8px;border:1px solid #eee;font-size:12px;color:{"#3ddc84" if v.startswith("✓") else "#ff5555"}">{v}</td></tr>'
        for k, v in RESULTS.items()
    ])
    html = f"""<html><body style="font-family:Arial,sans-serif;font-size:14px;color:#111;max-width:700px;margin:0 auto;padding:20px;">
<div style="background:#000;padding:20px 24px;border-radius:8px;margin-bottom:20px;">
  <div style="font-size:22px;color:#c9a84c;font-weight:700;letter-spacing:0.06em;">TECHNIK RENDERS</div>
  <div style="font-size:11px;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-top:4px;">Pipeline Complete · {now} SAST</div>
</div>

<h2 style="font-size:15px;margin:0 0 12px;">Today's Video</h2>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee;width:30%;font-weight:600">Title</td><td style="padding:8px;border:1px solid #eee">{idea.get('title','—')}</td></tr>
<tr><td style="padding:8px;border:1px solid #eee;font-weight:600">Car</td><td style="padding:8px;border:1px solid #eee">{idea.get('featured_car','—')}</td></tr>
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee;font-weight:600">Revenue type</td><td style="padding:8px;border:1px solid #eee">{idea.get('revenue_type','—')}</td></tr>
<tr><td style="padding:8px;border:1px solid #eee;font-weight:600">Affiliate</td><td style="padding:8px;border:1px solid #eee">{idea.get('affiliate_product','—')}</td></tr>
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee;font-weight:600">YouTube URL</td><td style="padding:8px;border:1px solid #eee"><a href="{video_url}" style="color:#1a73e8">{video_url}</a></td></tr>
</table>

<h2 style="font-size:15px;margin:0 0 12px;">AI Stack Used Today</h2>
<table style="width:100%;border-collapse:collapse;font-size:12px;margin-bottom:20px;">
<tr style="background:#000;color:#c9a84c"><td style="padding:8px 12px">Step</td><td style="padding:8px 12px">Tool</td><td style="padding:8px 12px">Status</td></tr>
<tr><td style="padding:8px;border:1px solid #eee">Prompt dev + Script + SEO + Social</td><td style="padding:8px;border:1px solid #eee">Claude</td><td style="padding:8px;border:1px solid #eee;color:#3ddc84">✓ Auto</td></tr>
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee">Image generation (6 images)</td><td style="padding:8px;border:1px solid #eee">NanoBanana Pro & 2</td><td style="padding:8px;border:1px solid #eee;color:#c9a84c">Manual — prompts in PRODUCTION_SHEET.txt</td></tr>
<tr><td style="padding:8px;border:1px solid #eee">Voiceover MP3</td><td style="padding:8px;border:1px solid #eee">ElevenLabs</td><td style="padding:8px;border:1px solid #eee;color:#3ddc84">✓ Auto</td></tr>
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee">Image enhancement</td><td style="padding:8px;border:1px solid #eee">Grok</td><td style="padding:8px;border:1px solid #eee;color:#c9a84c">Manual — enhance NanoBanana outputs</td></tr>
<tr><td style="padding:8px;border:1px solid #eee">Cinematic video clips (4 clips)</td><td style="padding:8px;border:1px solid #eee">Kling 3.0</td><td style="padding:8px;border:1px solid #eee;color:#c9a84c">Manual — prompts in PRODUCTION_SHEET.txt</td></tr>
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee">Hero opening sequence</td><td style="padding:8px;border:1px solid #eee">Higgsfield Cinema Studio</td><td style="padding:8px;border:1px solid #eee;color:#c9a84c">Manual — prompt in PRODUCTION_SHEET.txt</td></tr>
<tr><td style="padding:8px;border:1px solid #eee">Node-based edit + grade + captions</td><td style="padding:8px;border:1px solid #eee">Weavy</td><td style="padding:8px;border:1px solid #eee;color:#c9a84c">Manual — sequence in PRODUCTION_SHEET.txt</td></tr>
<tr style="background:#f9f9f9"><td style="padding:8px;border:1px solid #eee">YouTube upload + metadata</td><td style="padding:8px;border:1px solid #eee">YouTube API</td><td style="padding:8px;border:1px solid #eee;color:#3ddc84">✓ Auto (when video file present)</td></tr>
</table>

<h2 style="font-size:15px;margin:0 0 12px;">Pipeline Steps</h2>
<table style="width:100%;border-collapse:collapse;margin-bottom:20px;">{steps_html}</table>

<h2 style="font-size:15px;margin:0 0 12px;">Your Manual Steps (open PRODUCTION_SHEET.txt)</h2>
<ol style="font-size:13px;line-height:2.2;color:#333;">
<li>NanoBanana — run 6 image prompts → save as img_01 through img_06</li>
<li>Grok — enhance images before passing to Kling</li>
<li>Kling 3.0 — run 4 video prompts from enhanced images → save as clip_01 to clip_04</li>
<li>Higgsfield Cinema Studio — generate hero opening sequence → save as hero_sequence.mp4</li>
<li>Weavy — follow node edit sequence → export final_video.mp4</li>
<li>Canva — build 2 thumbnail variants → save thumbnail_A.jpg</li>
<li>Place final_video.mp4 in output/videos/ → run: python3 master.py → auto-uploads</li>
</ol>

<h2 style="font-size:15px;margin:0 0 12px;">Social Captions Ready</h2>
<div style="background:#f5f5f5;padding:14px;border-radius:6px;font-size:12px;font-family:'Courier New',monospace;white-space:pre-wrap;">INSTAGRAM:
{social.get('instagram_reel_caption','—')}

TIKTOK:
{social.get('tiktok_caption','—')}

X:
{social.get('x_post','—')}</div>

<p style="font-size:11px;color:#aaa;margin-top:24px;border-top:1px solid #eee;padding-top:12px;">
Technik Renders · Claude + NanoBanana + Kling 3.0 + Grok + Higgsfield + Weavy · logivo92@gmail.com
</p>
</body></html>"""

    GMAIL_USER = "logivo92@gmail.com"
    GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "")
    if GMAIL_PASS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Technik Renders — Pipeline Complete | {idea.get('title','')[:40]}"
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
        log("Report emailed to logivo92@gmail.com")
    else:
        with open("technik-pipeline/output/completion_report.html", "w") as f:
            f.write(html)
        log("Report saved to output/completion_report.html")

# ── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    log("\n" + "="*60)
    log("TECHNIK RENDERS — AUTONOMOUS PIPELINE v2")
    log("Stack: Claude → NanoBanana → Kling 3.0 + Grok + Higgsfield → Weavy")
    log("="*60 + "\n")
    setup()
    run_step("1. Idea generation",     generate_idea)
    run_step("2. Script writing",      write_script)
    run_step("3. Voiceover",           generate_voiceover)
    run_step("4. Creative briefs",     generate_creative_briefs)
    run_step("5. SEO package",         generate_seo)
    run_step("6. Social copy",         generate_social_copy)
    run_step("7. YouTube upload",      upload_to_youtube)
    run_step("8. Email report",        send_report)
    log("\n" + "="*60)
    log("PIPELINE COMPLETE:")
    for step, result in RESULTS.items():
        log(f"  {result}  {step}")
    log("="*60)
    log("Next: open output/renders/PRODUCTION_SHEET.txt")
