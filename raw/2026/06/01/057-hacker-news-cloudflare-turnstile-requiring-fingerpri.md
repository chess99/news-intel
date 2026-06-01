---
title: "Cloudflare Turnstile requiring fingerprintable WebGL"
source: Hacker News
url: https://hacktivis.me/articles/cloudflare-turnstile-webgl-fingerprinting
published: 2026-05-31T22:13:20+08:00
lang: en
category: community
fetched_at: 2026-06-01T17:14:22.320426+08:00
---

# Cloudflare Turnstile requiring fingerprintable WebGL

**来源**: Hacker News | **发布**: 2026-05-31 | **链接**: https://hacktivis.me/articles/cloudflare-turnstile-webgl-fingerprinting

## RSS 摘要

Comments

## 正文

Cloudflare Turnstile requiring fingerprintable WebGL published on 2026-05-30T23:31:51Z, last updated on 2026-05-30T23:31:52Z Since about a week, Cloudflare Turnstile (their "Verify you're human" device verification) has been looping indefinitely in my webkit-gtk based browser . Preventing access to quite few websites ( previously , but it even went worse lately). Turns out it's because Cloudflare wants to have a fingerprint of your device via WebGL, the only reason for doing this would be tracking. Screenshot of Turnstile test page , "WebGL renderer info is spoofed" Their pro-tracking non-justification copied here just in case: Turnstile uses browser fingerprinting to verify you're human. Privacy tools that block or randomize fingerprinting make your browser look like a bot trying to hide its identity. Temporarily allowing fingerprinting for this site will fix the issue. Such things are blocked in WebKit, and have been for years. Meaning it's tracking so awful that even Apple would block it, and as far as I can tell it's not the kind of privacy protection you can easily disable in it. So Cloudflare just banned all WebKitGTK browsers as I guess they put an exception for Safari. As an aside, if you're wondering, Mozilla Firefox screwed up their WebGL fingerprinting protection: Bugzilla#1916271: Gecko reveals sanitized GPU Characteristics; webkit and blink return hardcoded strings for all users Screenshot of Turnstile test page on Firefox 145.0 passing with no issues. Plus privacy.resistfingerprinting isn't enabled even when selecting "Strict" "Enhanced Privacy Protection" in the settings, great job there Mozilla. But I guess with it enabled, privacy-conscious Firefox users might not be able to pass Cloudflare's device verification in the future. Screenshot of Turnstile test page on Firefox 145.0 passing with just "Canvas Randomization Detected"; after enabling privacy.resistfingerprinting manually. Fediverse post for comments
