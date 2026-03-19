#!/usr/bin/env python3
"""
TECHNIK RENDERS — SOCIAL INTELLIGENCE + AUTO-POSTING SYSTEM
Pulls trending data, calculates optimal post times, posts automatically,
monitors analytics, and emails daily report to logivo92@gmail.com
Run: python3 social_engine.py
"""

import os, json, datetime, time, requests, smtplib, traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

LOG = "technik-pipeline/logs/social.log"
RESULTS = {}

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    os.makedirs("technik-pipeline/logs", exist_ok=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def load_env():
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

# ─────────────────────────────────────────────────────────────
# PHASE 1 — TRENDING INTELLIGENCE
# Pull what's hot RIGHT NOW across automotive + luxury content
# ─────────────────────────────────────────────────────────────

def get_trending_data():
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    # Pull Google Trends via SerpAPI (free tier available)
    trends = {}
    SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")

    if SERPAPI_KEY:
        try:
            # Google Trends — automotive
            r = requests.get("https://serpapi.com/search", params={
                "engine": "google_trends",
                "q": "luxury car,PPF,car detailing,supercar,Porsche,Lamborghini",
                "geo": "ZA",
                "api_key": SERPAPI_KEY
            }, timeout=10)
            if r.status_code == 200:
                trends["google"] = r.json().get("interest_over_time", {})
                log("Google Trends pulled")
        except Exception as e:
            log(f"Google Trends failed: {e}")

        try:
            # X / Twitter trending
            r = requests.get("https://serpapi.com/search", params={
                "engine": "twitter",
                "q": "luxury car OR supercar OR PPF OR cardetailing",
                "api_key": SERPAPI_KEY
            }, timeout=10)
            if r.status_code == 200:
                trends["x_trending"] = r.json().get("organic_results", [])[:10]
                log("X trends pulled")
        except Exception as e:
            log(f"X trends failed: {e}")

    # Use Claude to synthesise trending intelligence
    system = """You are a social media intelligence analyst for Technik Renders — 
    a cinematic automotive YouTube/Instagram/TikTok/X channel.
    Analyse what is trending RIGHT NOW in automotive content and provide 
    actionable intelligence. Output ONLY valid JSON."""

    today = datetime.date.today().strftime("%B %d, %Y")
    prompt = f"""Today is {today}. Generate trending intelligence for automotive content.
    
    Return JSON:
    {{
      "trending_topics": [
        {{"topic": "topic name", "platform": "YouTube|Instagram|TikTok|X", "momentum": "rising|peak|declining", "content_angle": "how to use this"}}
      ],
      "trending_hashtags": {{
        "instagram": ["#tag1","#tag2","#tag3","#tag4","#tag5","#tag6","#tag7","#tag8","#tag9","#tag10"],
        "tiktok": ["#tag1","#tag2","#tag3","#tag4","#tag5"],
        "x": ["#tag1","#tag2","#tag3"]
      }},
      "viral_hooks_today": [
        "hook line 1 trending in automotive",
        "hook line 2",
        "hook line 3"
      ],
      "avoid_today": ["topic that is oversaturated", "topic with low engagement"],
      "platform_notes": {{
        "youtube": "what is working on YouTube automotive right now",
        "instagram": "what is working on Instagram automotive right now", 
        "tiktok": "what is working on TikTok automotive right now",
        "x": "what is working on X automotive right now"
      }}
    }}"""

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=system,
        messages=[{"role": "user", "content": prompt}]
    )

    intelligence = json.loads(msg.content[0].text)
    intelligence["pulled_at"] = datetime.datetime.now().isoformat()
    intelligence["raw_trends"] = trends

    with open("technik-pipeline/output/social/trending_intelligence.json", "w") as f:
        json.dump(intelligence, f, indent=2)

    log(f"Trending topics: {[t['topic'] for t in intelligence['trending_topics'][:3]]}")
    return intelligence

# ─────────────────────────────────────────────────────────────
# PHASE 2 — OPTIMAL POSTING SCHEDULE
# Algorithm-aware timing for maximum reach
# ─────────────────────────────────────────────────────────────

def calculate_posting_schedule():
    """
    Peak posting windows based on platform algorithms + Johannesburg timezone (SAST = UTC+2)
    Research-backed optimal times for automotive/luxury content
    """

    now = datetime.datetime.now()
    today = now.date()

    # Algorithm-backed peak windows (SAST)
    PEAK_WINDOWS = {
        "youtube": [
            {"time": "08:00", "reason": "Morning commute — high search intent"},
            {"time": "12:00", "reason": "Lunch break browsing peak"},
            {"time": "17:00", "reason": "After-work — highest watch time"},
            {"time": "20:00", "reason": "Prime time — longest sessions"},
        ],
        "instagram": [
            {"time": "07:00", "reason": "Pre-work scroll — high engagement"},
            {"time": "11:00", "reason": "Mid-morning peak"},
            {"time": "16:00", "reason": "After school/work"},
            {"time": "19:00", "reason": "Evening prime — best Reel distribution"},
        ],
        "tiktok": [
            {"time": "07:00", "reason": "Morning routine scroll"},
            {"time": "13:00", "reason": "Lunch break — viral window"},
            {"time": "19:00", "reason": "Evening peak — algorithm pushes hard"},
            {"time": "22:00", "reason": "Late night — Gen Z prime time"},
        ],
        "x": [
            {"time": "08:00", "reason": "Business hour start — news scroll"},
            {"time": "12:00", "reason": "Lunch — trending window"},
            {"time": "17:00", "reason": "End of work — engagement spike"},
            {"time": "20:00", "reason": "Evening discussion peak"},
        ]
    }

    # Calculate next optimal slot for each platform
    schedule = {}
    for platform, windows in PEAK_WINDOWS.items():
        next_slots = []
        for w in windows:
            hour, minute = map(int, w["time"].split(":"))
            slot_dt = datetime.datetime.combine(today, datetime.time(hour, minute))
            if slot_dt < now:
                slot_dt += datetime.timedelta(days=1)
            next_slots.append({
                "datetime": slot_dt.isoformat(),
                "time_sast": w["time"],
                "reason": w["reason"],
                "minutes_until": int((slot_dt - now).total_seconds() / 60)
            })
        # Sort by soonest
        next_slots.sort(key=lambda x: x["minutes_until"])
        schedule[platform] = {
            "next_post": next_slots[0],
            "all_windows_today": next_slots
        }

    # Best day strategy
    DAY_STRATEGY = {
        0: "Monday — post motivational angle, 'week in cars' content",
        1: "Tuesday — technical content, 'how it works' performs well",
        2: "Wednesday — comparison content, mid-week algorithm boost",
        3: "Thursday — trending/news angle, pre-weekend build",
        4: "Friday — aspirational content, 'weekend drive' energy",
        5: "Saturday — luxury showcase, highest organic reach",
        6: "Sunday — reflective/educational, high watch time"
    }

    schedule["today_strategy"] = DAY_STRATEGY[now.weekday()]
    schedule["timezone"] = "SAST (UTC+2)"
    schedule["generated_at"] = now.isoformat()

    with open("technik-pipeline/output/social/posting_schedule.json", "w") as f:
        json.dump(schedule, f, indent=2)

    log(f"Schedule calculated — Today: {schedule['today_strategy']}")
    log(f"Next YouTube window: {schedule['youtube']['next_post']['time_sast']} SAST")
    log(f"Next Instagram window: {schedule['instagram']['next_post']['time_sast']} SAST")
    return schedule

# ─────────────────────────────────────────────────────────────
# PHASE 3 — POST TO X (Twitter API v2)
# ─────────────────────────────────────────────────────────────

def post_to_x(content: dict, video_url: str = "") -> dict:
    try:
        import tweepy

        client = tweepy.Client(
            consumer_key=os.environ["X_API_KEY"],
            consumer_secret=os.environ["X_API_SECRET"],
            access_token=os.environ["X_ACCESS_TOKEN"],
            access_token_secret=os.environ["X_ACCESS_SECRET"]
        )

        # Build post text
        text = content.get("x_post", "")
        if video_url:
            text = text.replace("[YOUTUBE_LINK]", video_url)
        else:
            text = text.replace("[YOUTUBE_LINK]", "").strip()

        # Ensure under 280 chars
        if len(text) > 280:
            text = text[:277] + "..."

        tweet = client.create_tweet(text=text)
        tweet_id = tweet.data["id"]
        tweet_url = f"https://x.com/i/web/status/{tweet_id}"

        log(f"X posted: {tweet_url}")
        return {"status": "posted", "url": tweet_url, "id": tweet_id}

    except Exception as e:
        log(f"X post failed: {e}")
        return {"status": "failed", "error": str(e)}

# ─────────────────────────────────────────────────────────────
# PHASE 4 — POST TO INSTAGRAM (Meta Graph API)
# ─────────────────────────────────────────────────────────────

def post_to_instagram(content: dict, trending: dict, reel_url: str = "") -> dict:
    try:
        user_id = os.environ["INSTAGRAM_USER_ID"]
        token   = os.environ["INSTAGRAM_ACCESS_TOKEN"]

        # Build caption with trending hashtags
        caption = content.get("instagram_reel_caption", "")
        trending_tags = " ".join(trending.get("trending_hashtags", {}).get("instagram", [])[:10])
        if trending_tags and trending_tags not in caption:
            caption += f"\n\n{trending_tags}"

        if not reel_url:
            log("Instagram: no Reel video URL — saving caption for manual post")
            with open("technik-pipeline/output/social/instagram_caption_pending.txt", "w") as f:
                f.write(caption)
            return {"status": "pending_video", "caption_saved": True}

        # Step 1: Create media container
        create_resp = requests.post(
            f"https://graph.facebook.com/v18.0/{user_id}/reels",
            data={
                "video_url": reel_url,
                "caption": caption,
                "access_token": token
            }
        ).json()

        creation_id = create_resp.get("id")
        if not creation_id:
            return {"status": "failed", "error": create_resp}

        # Step 2: Wait for processing (Instagram needs ~30 sec)
        log("Instagram: waiting for video processing...")
        time.sleep(35)

        # Step 3: Check status
        status_resp = requests.get(
            f"https://graph.facebook.com/v18.0/{creation_id}",
            params={"fields": "status_code", "access_token": token}
        ).json()

        if status_resp.get("status_code") == "FINISHED":
            # Step 4: Publish
            pub_resp = requests.post(
                f"https://graph.facebook.com/v18.0/{user_id}/media_publish",
                data={"creation_id": creation_id, "access_token": token}
            ).json()
            post_id = pub_resp.get("id")
            log(f"Instagram Reel published: {post_id}")
            return {"status": "posted", "id": post_id}
        else:
            return {"status": "failed", "error": f"Video status: {status_resp}"}

    except Exception as e:
        log(f"Instagram failed: {e}")
        return {"status": "failed", "error": str(e)}

# ─────────────────────────────────────────────────────────────
# PHASE 5 — POST TO TIKTOK (Content Posting API)
# ─────────────────────────────────────────────────────────────

def post_to_tiktok(content: dict, trending: dict, video_path: str = "") -> dict:
    try:
        token = os.environ.get("TIKTOK_ACCESS_TOKEN", "")
        if not token:
            log("TikTok: no access token — caption saved for manual post")
            caption = content.get("tiktok_caption", "")
            trending_tags = " ".join(trending.get("trending_hashtags", {}).get("tiktok", []))
            full_caption = f"{caption} {trending_tags}".strip()
            with open("technik-pipeline/output/social/tiktok_caption_pending.txt", "w") as f:
                f.write(full_caption)
            return {"status": "pending_manual", "caption_saved": True}

        # TikTok Content Posting API
        caption = content.get("tiktok_caption", "")
        trending_tags = " ".join(trending.get("trending_hashtags", {}).get("tiktok", []))
        full_caption = f"{caption} {trending_tags}".strip()[:2200]

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        if video_path and os.path.exists(video_path):
            # Direct post with video file
            init_resp = requests.post(
                "https://open.tiktokapis.com/v2/post/publish/video/init/",
                headers=headers,
                json={
                    "post_info": {
                        "title": full_caption,
                        "privacy_level": "PUBLIC_TO_EVERYONE",
                        "disable_duet": False,
                        "disable_comment": False,
                        "disable_stitch": False,
                        "video_cover_timestamp_ms": 1000
                    },
                    "source_info": {
                        "source": "FILE_UPLOAD",
                        "video_size": os.path.getsize(video_path),
                        "chunk_size": os.path.getsize(video_path),
                        "total_chunk_count": 1
                    }
                }
            ).json()

            publish_id = init_resp.get("data", {}).get("publish_id")
            upload_url = init_resp.get("data", {}).get("upload_url")

            if upload_url:
                with open(video_path, "rb") as f:
                    video_data = f.read()
                upload_resp = requests.put(
                    upload_url,
                    headers={
                        "Content-Type": "video/mp4",
                        "Content-Length": str(len(video_data)),
                        "Content-Range": f"bytes 0-{len(video_data)-1}/{len(video_data)}"
                    },
                    data=video_data
                )
                log(f"TikTok upload: {upload_resp.status_code}")
                return {"status": "posted", "publish_id": publish_id}
        else:
            log("TikTok: no video file — caption saved for manual upload")
            with open("technik-pipeline/output/social/tiktok_caption_pending.txt", "w") as f:
                f.write(full_caption)
            return {"status": "pending_video", "caption_saved": True}

    except Exception as e:
        log(f"TikTok failed: {e}")
        return {"status": "failed", "error": str(e)}

# ─────────────────────────────────────────────────────────────
# PHASE 6 — ANALYTICS COLLECTION
# Pull performance data from all platforms
# ─────────────────────────────────────────────────────────────

def collect_analytics() -> dict:
    analytics = {
        "collected_at": datetime.datetime.now().isoformat(),
        "youtube": {},
        "instagram": {},
        "x": {},
        "tiktok": {}
    }

    # YouTube Analytics
    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = Credentials(
            token=None,
            refresh_token=os.environ.get("YOUTUBE_REFRESH_TOKEN", ""),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.environ.get("YOUTUBE_CLIENT_ID", ""),
            client_secret=os.environ.get("YOUTUBE_CLIENT_SECRET", ""),
            scopes=["https://www.googleapis.com/auth/youtube.readonly",
                    "https://www.googleapis.com/auth/yt-analytics.readonly"]
        )
        if creds.refresh_token:
            creds.refresh(Request())

            youtube = build("youtube", "v3", credentials=creds)

            # Channel stats
            channel = youtube.channels().list(
                part="statistics,snippet",
                mine=True
            ).execute()

            if channel["items"]:
                stats = channel["items"][0]["statistics"]
                analytics["youtube"] = {
                    "subscribers": int(stats.get("subscriberCount", 0)),
                    "total_views": int(stats.get("viewCount", 0)),
                    "total_videos": int(stats.get("videoCount", 0)),
                    "channel_name": channel["items"][0]["snippet"]["title"]
                }

            # Latest video performance
            videos = youtube.videos().list(
                part="statistics,snippet",
                myRating="none",
                chart="mostPopular",
                maxResults=5
            ).execute()

            # Get own channel's recent videos
            search = youtube.search().list(
                part="id,snippet",
                forMine=True,
                type="video",
                order="date",
                maxResults=3
            ).execute()

            recent_videos = []
            for item in search.get("items", []):
                vid_id = item["id"]["videoId"]
                vid_stats = youtube.videos().list(
                    part="statistics",
                    id=vid_id
                ).execute()
                if vid_stats["items"]:
                    s = vid_stats["items"][0]["statistics"]
                    recent_videos.append({
                        "title": item["snippet"]["title"][:50],
                        "views": int(s.get("viewCount", 0)),
                        "likes": int(s.get("likeCount", 0)),
                        "comments": int(s.get("commentCount", 0)),
                        "published": item["snippet"]["publishedAt"][:10]
                    })
            analytics["youtube"]["recent_videos"] = recent_videos
            log(f"YouTube: {analytics['youtube'].get('subscribers', 0)} subscribers")
    except Exception as e:
        analytics["youtube"]["error"] = str(e)
        log(f"YouTube analytics failed: {e}")

    # Instagram Analytics
    try:
        user_id = os.environ.get("INSTAGRAM_USER_ID", "")
        token   = os.environ.get("INSTAGRAM_ACCESS_TOKEN", "")
        if user_id and token:
            # Account insights
            r = requests.get(
                f"https://graph.facebook.com/v18.0/{user_id}",
                params={
                    "fields": "followers_count,media_count,name,username",
                    "access_token": token
                }
            ).json()
            analytics["instagram"] = {
                "followers": r.get("followers_count", 0),
                "posts": r.get("media_count", 0),
                "username": r.get("username", ""),
                "name": r.get("name", "")
            }

            # Recent media performance
            media = requests.get(
                f"https://graph.facebook.com/v18.0/{user_id}/media",
                params={
                    "fields": "id,caption,media_type,timestamp,like_count,comments_count",
                    "limit": 5,
                    "access_token": token
                }
            ).json()

            recent_posts = []
            for post in media.get("data", [])[:3]:
                recent_posts.append({
                    "type": post.get("media_type"),
                    "likes": post.get("like_count", 0),
                    "comments": post.get("comments_count", 0),
                    "date": post.get("timestamp", "")[:10]
                })
            analytics["instagram"]["recent_posts"] = recent_posts
            log(f"Instagram: {analytics['instagram'].get('followers', 0)} followers")
    except Exception as e:
        analytics["instagram"]["error"] = str(e)
        log(f"Instagram analytics failed: {e}")

    # X Analytics
    try:
        import tweepy
        client = tweepy.Client(
            consumer_key=os.environ.get("X_API_KEY", ""),
            consumer_secret=os.environ.get("X_API_SECRET", ""),
            access_token=os.environ.get("X_ACCESS_TOKEN", ""),
            access_token_secret=os.environ.get("X_ACCESS_SECRET", "")
        )
        me = client.get_me(user_fields=["public_metrics", "name", "username"])
        if me.data:
            metrics = me.data.public_metrics
            analytics["x"] = {
                "followers": metrics["followers_count"],
                "following": metrics["following_count"],
                "tweets": metrics["tweet_count"],
                "username": me.data.username,
                "name": me.data.name
            }

            # Recent tweets performance
            tweets = client.get_users_tweets(
                id=me.data.id,
                max_results=5,
                tweet_fields=["public_metrics", "created_at"]
            )
            recent_tweets = []
            if tweets.data:
                for tweet in tweets.data[:3]:
                    m = tweet.public_metrics
                    recent_tweets.append({
                        "likes": m["like_count"],
                        "retweets": m["retweet_count"],
                        "replies": m["reply_count"],
                        "impressions": m.get("impression_count", 0),
                        "date": str(tweet.created_at)[:10]
                    })
            analytics["x"]["recent_tweets"] = recent_tweets
            log(f"X: {analytics['x'].get('followers', 0)} followers")
    except Exception as e:
        analytics["x"]["error"] = str(e)
        log(f"X analytics failed: {e}")

    with open("technik-pipeline/output/social/analytics.json", "w") as f:
        json.dump(analytics, f, indent=2)

    return analytics

# ─────────────────────────────────────────────────────────────
# PHASE 7 — DAILY REPORT EMAIL
# Everything you need to see in one email
# ─────────────────────────────────────────────────────────────

def send_daily_report(analytics: dict, schedule: dict, trending: dict, post_results: dict):
    now = datetime.datetime.now().strftime("%d %B %Y, %H:%M")

    yt = analytics.get("youtube", {})
    ig = analytics.get("instagram", {})
    x  = analytics.get("x", {})

    # Recent videos table
    recent_vids_html = ""
    for v in yt.get("recent_videos", []):
        recent_vids_html += f"""
        <tr>
          <td style="padding:8px;border:1px solid #eee;font-size:12px">{v['title']}</td>
          <td style="padding:8px;border:1px solid #eee;text-align:center">{v['views']:,}</td>
          <td style="padding:8px;border:1px solid #eee;text-align:center">{v['likes']:,}</td>
          <td style="padding:8px;border:1px solid #eee;text-align:center">{v['date']}</td>
        </tr>"""

    # Trending topics
    trending_html = ""
    for t in trending.get("trending_topics", [])[:5]:
        momentum_color = "#3ddc84" if t['momentum'] == 'rising' else "#c9a84c" if t['momentum'] == 'peak' else "#888"
        trending_html += f"""
        <tr>
          <td style="padding:8px;border:1px solid #eee;font-weight:600">{t['topic']}</td>
          <td style="padding:8px;border:1px solid #eee">{t['platform']}</td>
          <td style="padding:8px;border:1px solid #eee;color:{momentum_color};font-weight:600">{t['momentum'].upper()}</td>
          <td style="padding:8px;border:1px solid #eee;font-size:12px">{t['content_angle']}</td>
        </tr>"""

    # Post schedule
    sched_html = ""
    for platform in ["youtube", "instagram", "tiktok", "x"]:
        s = schedule.get(platform, {})
        if s:
            next_p = s.get("next_post", {})
            sched_html += f"""
            <tr>
              <td style="padding:8px;border:1px solid #eee;font-weight:600;text-transform:capitalize">{platform}</td>
              <td style="padding:8px;border:1px solid #eee">{next_p.get('time_sast','—')} SAST</td>
              <td style="padding:8px;border:1px solid #eee;font-size:12px">{next_p.get('reason','—')}</td>
            </tr>"""

    # Post results
    results_html = ""
    for platform, result in post_results.items():
        status = result.get("status", "unknown")
        color = "#3ddc84" if status == "posted" else "#c9a84c" if "pending" in status else "#ff5555"
        results_html += f"""
        <tr>
          <td style="padding:8px;border:1px solid #eee;font-weight:600">{platform}</td>
          <td style="padding:8px;border:1px solid #eee;color:{color};font-weight:600">{status.upper()}</td>
          <td style="padding:8px;border:1px solid #eee;font-size:12px">{result.get('url', result.get('id', result.get('error', '—')))}</td>
        </tr>"""

    # Trending hashtags
    ig_tags = " ".join(trending.get("trending_hashtags", {}).get("instagram", []))
    tt_tags = " ".join(trending.get("trending_hashtags", {}).get("tiktok", []))
    x_tags  = " ".join(trending.get("trending_hashtags", {}).get("x", []))

    html = f"""<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;font-size:14px;color:#111;max-width:760px;margin:0 auto;padding:20px;line-height:1.6;">

<div style="background:#000;padding:20px 24px;border-radius:8px;margin-bottom:24px;">
  <div style="font-family:Georgia,serif;font-size:24px;color:#c9a84c;letter-spacing:0.1em;font-weight:700;">TECHNIK RENDERS</div>
  <div style="font-size:11px;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-top:4px;">Daily Intelligence Report · {now} SAST</div>
</div>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Platform Overview</h2>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-bottom:24px;">
  <div style="background:#f9f9f9;border:1px solid #eee;border-radius:8px;padding:14px;text-align:center;">
    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">YouTube</div>
    <div style="font-size:28px;font-weight:700;color:#c9a84c">{yt.get('subscribers',0):,}</div>
    <div style="font-size:11px;color:#888">subscribers</div>
    <div style="font-size:12px;color:#555;margin-top:6px">{yt.get('total_views',0):,} total views</div>
  </div>
  <div style="background:#f9f9f9;border:1px solid #eee;border-radius:8px;padding:14px;text-align:center;">
    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Instagram</div>
    <div style="font-size:28px;font-weight:700;color:#c9a84c">{ig.get('followers',0):,}</div>
    <div style="font-size:11px;color:#888">followers</div>
    <div style="font-size:12px;color:#555;margin-top:6px">@{ig.get('username','—')}</div>
  </div>
  <div style="background:#f9f9f9;border:1px solid #eee;border-radius:8px;padding:14px;text-align:center;">
    <div style="font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">X</div>
    <div style="font-size:28px;font-weight:700;color:#c9a84c">{x.get('followers',0):,}</div>
    <div style="font-size:11px;color:#888">followers</div>
    <div style="font-size:12px;color:#555;margin-top:6px">@{x.get('username','—')}</div>
  </div>
</div>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Today's Strategy · {schedule.get('today_strategy','—')}</h2>

<h2 style="font-size:15px;margin:20px 0 12px;color:#333;">Trending Now — Act On These Today</h2>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <tr style="background:#000;color:#c9a84c;"><td style="padding:8px 12px;">Topic</td><td style="padding:8px 12px;">Platform</td><td style="padding:8px 12px;">Momentum</td><td style="padding:8px 12px;">Use It Like This</td></tr>
  {trending_html}
</table>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Trending Hashtags (use these today)</h2>
<div style="background:#f5f5f5;border-radius:6px;padding:14px;font-size:12px;margin-bottom:20px;">
  <div style="margin-bottom:8px;"><strong>Instagram:</strong> {ig_tags}</div>
  <div style="margin-bottom:8px;"><strong>TikTok:</strong> {tt_tags}</div>
  <div><strong>X:</strong> {x_tags}</div>
</div>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Viral Hooks Trending Today</h2>
<ul style="font-size:13px;line-height:2;color:#333;background:#f5f5f5;border-radius:6px;padding:14px 14px 14px 30px;margin-bottom:20px;">
  {''.join([f'<li>{h}</li>' for h in trending.get('viral_hooks_today',[])])}
</ul>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Optimal Posting Windows (SAST)</h2>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <tr style="background:#000;color:#c9a84c;"><td style="padding:8px 12px;">Platform</td><td style="padding:8px 12px;">Next Post</td><td style="padding:8px 12px;">Why</td></tr>
  {sched_html}
</table>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Today's Post Results</h2>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <tr style="background:#000;color:#c9a84c;"><td style="padding:8px 12px;">Platform</td><td style="padding:8px 12px;">Status</td><td style="padding:8px 12px;">Detail</td></tr>
  {results_html if results_html else '<tr><td colspan="3" style="padding:12px;text-align:center;color:#888;">No posts made today — pipeline ran content generation only</td></tr>'}
</table>

<h2 style="font-size:15px;margin:0 0 12px;color:#333;">Recent YouTube Videos</h2>
<table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:20px;">
  <tr style="background:#000;color:#c9a84c;"><td style="padding:8px 12px;">Title</td><td style="padding:8px 12px;text-align:center;">Views</td><td style="padding:8px 12px;text-align:center;">Likes</td><td style="padding:8px 12px;text-align:center;">Date</td></tr>
  {recent_vids_html if recent_vids_html else '<tr><td colspan="4" style="padding:12px;text-align:center;color:#888;">No videos yet</td></tr>'}
</table>

<div style="background:#000;border-radius:6px;padding:16px 20px;margin-top:24px;">
  <div style="font-size:11px;color:#555;letter-spacing:0.08em;text-transform:uppercase;">Platform Notes</div>
  <div style="margin-top:10px;font-size:13px;color:#ccc;line-height:1.8;">
    <div><strong style="color:#c9a84c;">YouTube:</strong> {trending.get('platform_notes',{}).get('youtube','—')}</div>
    <div><strong style="color:#c9a84c;">Instagram:</strong> {trending.get('platform_notes',{}).get('instagram','—')}</div>
    <div><strong style="color:#c9a84c;">TikTok:</strong> {trending.get('platform_notes',{}).get('tiktok','—')}</div>
    <div><strong style="color:#c9a84c;">X:</strong> {trending.get('platform_notes',{}).get('x','—')}</div>
  </div>
</div>

<p style="font-size:11px;color:#aaa;margin-top:20px;border-top:1px solid #eee;padding-top:12px;">
  Technik Renders · Automated by Claude AI + Manus · logivo92@gmail.com
</p>
</body>
</html>"""

    GMAIL_USER = "logivo92@gmail.com"
    GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "")

    if GMAIL_PASS:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Technik Renders · Daily Report · {datetime.date.today().strftime('%d %b %Y')}"
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER
        msg.attach(MIMEText(html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(GMAIL_USER, GMAIL_PASS)
            s.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
        log("Daily report emailed to logivo92@gmail.com")
    else:
        with open("technik-pipeline/output/social/daily_report.html", "w") as f:
            f.write(html)
        log("Report saved to output/social/daily_report.html")

# ─────────────────────────────────────────────────────────────
# MAIN — Run everything
# ─────────────────────────────────────────────────────────────

def run_step(name, fn, *args, **kwargs):
    log(f"▶ {name}")
    try:
        result = fn(*args, **kwargs)
        RESULTS[name] = "✓"
        log(f"✓ {name} complete")
        return result
    except Exception as e:
        RESULTS[name] = f"✗ {str(e)[:60]}"
        log(f"✗ {name} failed: {e}")
        traceback.print_exc()
        return {}

if __name__ == "__main__":
    log("\n" + "="*60)
    log("TECHNIK RENDERS — SOCIAL INTELLIGENCE ENGINE")
    log("="*60)

    load_env()
    os.makedirs("technik-pipeline/output/social", exist_ok=True)

    # Load today's content if pipeline was run
    content = {}
    if os.path.exists("technik-pipeline/output/social/social_copy.json"):
        with open("technik-pipeline/output/social/social_copy.json") as f:
            content = json.load(f)

    video_url = ""
    if os.path.exists("technik-pipeline/output/video_url.txt"):
        with open("technik-pipeline/output/video_url.txt") as f:
            video_url = f.read().strip()

    reel_url  = os.environ.get("REEL_VIDEO_URL", "")
    tiktok_video = "technik-pipeline/output/videos/tiktok_clip.mp4"

    # Run all phases
    trending  = run_step("Trending intelligence",    get_trending_data)
    schedule  = run_step("Posting schedule",         calculate_posting_schedule)
    analytics = run_step("Collect analytics",        collect_analytics)

    post_results = {}
    if content:
        post_results["X"]         = run_step("Post to X",         post_to_x,         content, video_url) or {}
        post_results["Instagram"] = run_step("Post to Instagram", post_to_instagram,  content, trending, reel_url) or {}
        post_results["TikTok"]    = run_step("Post to TikTok",    post_to_tiktok,     content, trending, tiktok_video) or {}
    else:
        log("No social content found — run run_pipeline.py first to generate content")

    run_step("Send daily report", send_daily_report, analytics, schedule, trending, post_results)

    log("\n" + "="*60)
    log("SOCIAL ENGINE COMPLETE")
    for step, r in RESULTS.items():
        log(f"  {r}  {step}")
    log("="*60)
