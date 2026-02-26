🌐 Complete API Integration Guide for Social Listening Engine

A step-by-step guide to connect your engine to real social media data from Reddit, Twitter/X, and Meta (Facebook/Instagram).
📋 What This Guide Covers

    Getting API keys from each platform

    Setting up configuration files safely

    How data flows through your existing pipeline

    What features you can add with real data

    Tips for staying within rate limits

#🔑 Part 1: Getting API Keys
Reddit API

    Go to https://www.reddit.com/prefs/apps

    Click "create app" at the bottom

    Choose "script" (not web app)

    Fill in:

        name: "SocialListeningEngine" (or anything)

        description: optional

        about url: your GitHub repo URL

        redirect uri: http://localhost:8000 (doesn't matter for script apps)

    Click "create app"

    You'll see:

        client_id: the string under your app name (looks like random letters/numbers)

        client_secret: listed as "secret"

Twitter/X API v2

    Go to https://developer.twitter.com/en/portal/dashboard

    Sign up for a developer account (may take 1-2 days approval)

    Create a Project → name it "SocialListeningEngine"

    Create an App within the project

    Go to "Keys and tokens" tab

    Generate Bearer Token (for read-only access) — copy this

    (Optional) Generate API Key/Secret if you need to post

Meta (Facebook/Instagram) API

    Go to https://developers.facebook.com/

    Click "My Apps" → "Create App"

    Choose "Business" as app type

    Fill in basic info

    Once created, go to Dashboard → add "Instagram Basic Display" or "Facebook Page API"

    Generate access token (needs pages_read_engagement permission)

    Copy your Page ID (from your Facebook page's About section)

#🔐 Part 2: Setting Up Configuration (Safe Way)

Never hardcode API keys! Use environment variables or config files.
Create a template file (safe to commit):

Create config/api_config.yaml.example:

```
# Copy this file to api_config.yaml and add your real keys
# DO NOT commit api_config.yaml to GitHub!

reddit:
  client_id: "your_client_id_here"
  client_secret: "your_secret_here"
  user_agent: "SocialListeningEngine/1.0 (by u/your_username)"

twitter:
  bearer_token: "your_bearer_token_here"

meta:
  access_token: "your_access_token_here"
  page_id: "your_page_id_here"
  instagram_user_id: "your_ig_user_id_here"  # for Instagram
```

Create the real config (DO NOT commit this):

Copy the example and add your keys:
```
cp config/api_config.yaml.example config/api_config.yaml
# Then edit with your real keys
```

Protect your keys:

Add to .gitignore:
```
config/api_config.yaml
.env
*.key
```

#📦 Part 3: Installing Required Packages

Add these to your requirements.txt:
```
praw==7.7.1           # Reddit API
tweepy>=4.14.0        # Twitter API
requests>=2.31.0      # For Meta API
python-dotenv>=1.0.0  # For environment variables
pyyaml>=6.0           # For reading config files
```
Install with:
```
pip install -r requirements.txt
```

#🔄 Part 4: How Real Data Flows Through Your Pipeline
Your current pipeline (tweet_eval):
```
Hugging Face → DataFrame → text_cleaner.py → intent_classifier.py → vector_search.py → topic_modeling.py → gradio_app.py
```
With real APIs:
```
Reddit/Twitter/Meta → DataFrame + metadata → text_cleaner.py → [rest of pipeline stays IDENTICAL]
```
Everything after the first step stays exactly the same. Our existing code doesn't care where the text came from.

#📊 Part 5: New Data Features You Can Add

Real APIs give you metadata that tweet_eval didn't have:
From Reddit:

    Upvotes/downvotes

    Comment count

    Subreddit name

    Author reputation (karma)

    Whether it's a link vs text post

From Twitter/X:

    Like count

    Retweet count

    Reply count

    Whether it's a quote tweet

    Verified status

From Meta:

    Post reactions (likes, loves, etc)

    Comment count

    Share count

    Post type (photo, video, link)

New features you can create:

    Engagement score: (likes + comments) / followers (if available)

    Post length: short vs long posts behave differently

    Hashtag count: more hashtags = more promotional

    Time features: hour of day, day of week, weekend vs weekday

    Author influence: based on follower count or karma

#🧠 Part 6: What New Insights You Can Get
Question	Without API	With API

What's trending?	        ✅ Yes	    ✅ Yes

What's the sentiment?	    ✅ Yes	    ✅ Yes

Who's complaining most?	    ❌ No	    ✅ Can track by author

Which posts go viral?	    ❌ No	    ✅ Can rank by engagement

Best time to post?	        ❌ No	    ✅ Can analyze hourly trends

Are influencers different?	❌ No	    ✅ Can segment by follower count

#⏱️ Part 7: Rate Limits & Ethical Use
Reddit API limits:

    60 requests per minute

    Use praw which handles this automatically

    Cache results to avoid repeated calls

Twitter API limits:

    Free tier: 500k tweets per month

    450 requests per 15-minute window

    Use tweepy which respects limits

Meta API limits:

    200 calls per hour per user

    Slower, but fine for demos

Best practices:

    Cache aggressively — save results locally so you don't re-fetch

    Add delays between requests if hitting limits

    Respect user privacy — don't store PII (personally identifiable info)

    Follow platform terms — don't use for surveillance or harassment

#📁 Part 8: New Files to Add to Your Project
src/data_loader.py

Contains classes for each platform that:

    Load config

    Connect to API

    Fetch posts

    Convert to your DataFrame format

    Add metadata columns

    Apply your existing cleaning functions
```
config/api_config.yaml.example
```
Template for users to copy (safe to commit)
```
docs/API_INTEGRATION.md
```
This entire guide — so users know how to connect their own APIs
```
notebooks/api_demo.ipynb (optional)
```
A notebook showing step-by-step how to fetch and process live data


#🚀 Part 9: Quick Start for Users

   Get API keys from Reddit/Twitter/Meta (see Part 1)

   Copy the config template:    
```
    cp config/api_config.yaml.example config/api_config.yaml
```
  Add your keys to config/api_config.yaml

  Install extra packages:
```
  pip install praw tweepy requests python-dotenv pyyaml
```
  Run the data loader:
```
    from src.data_loader import RedditLoader
    loader = RedditLoader()
    df = loader.search_posts("your query", limit=100)
```
  Feed into your existing pipeline — everything else just works!

#⚠️ Part 10: Common Issues & Solutions

Problem	Solution
"praw not found"	Install: pip install praw
"Invalid credentials"	Check your api_config.yaml — keys are case sensitive
"Rate limit exceeded"	Add time.sleep(1) between requests or use caching
"Missing timestamps"	Convert API timestamps to pandas datetime: pd.to_datetime()
"Text too long"	Reddit posts can be long — your cleaning functions handle this fine
"Emoji/unusual chars"	Your clean_for_topics removes non-letters, so safe

📚 Part 11: Helpful Resources

  PRAW docs: https://praw.readthedocs.io/

  Tweepy docs: https://docs.tweepy.org/

  Meta Graph API: https://developers.facebook.com/docs/graph-api/

  Python-dotenv: https://github.com/theskumar/python-dotenv

  Rate limit calculator: https://github.com/jamesturk/ratelimit

#🎯 Part 12: What Your Users Will Learn

By following this guide, users will be able to:

  Connect to three major social platforms

  Safely store API keys without exposing them

  Fetch real data into their existing pipeline

  Enrich analysis with engagement metrics

  Respect rate limits and API terms

  Adapt the code to any text-based social platform
