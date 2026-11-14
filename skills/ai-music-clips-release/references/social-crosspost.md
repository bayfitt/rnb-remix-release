# Verified Instagram and TikTok releases

On November 13, 2026 (America/New_York), the two full-length releases in the [recipe index](../../../releases/README.md) were published to both platforms. All four posts are public. Their complete intros, separate visuals and large timed lyric captions were retained; no new music was generated for this cross-post.

## Instagram

The `instagram-tools` CLI published both Reels through instagrapi 3.2.12. Each private receipt records the returned media identifier and successful verification of the intended owner and exact caption. Independent probes of the published media found H.264 video at 720 × 1280 with AAC audio and durations of approximately 197 and 252 seconds, matching the full edits with ordinary encoding differences.

The captions include source attribution, explicit AI disclosure and pinned complete remix recipes. The profile's AI-generated label was visible during verification. The helper does not set a native per-post AI-content flag; a profile label or caption must not be represented as that flag. Live comments and insights checks remain untested.

## TikTok

The rebuilt uploader placed the first video in a draft but stopped at an onboarding overlay. That draft was resumed through the browser-harness CLI controlling the existing authorized Chrome session. The second video was uploaded through the same browser interface. This was a fallback and does not validate end-to-end publishing with the rebuilt uploader's `--ai-generated` option.

For each post, the account, full source file, custom cover, exact caption and complete recipe link were checked. The native **AI-generated content** switch and **Your brand** disclosure were enabled before Post. Both published videos show **Creator labeled as AI-generated**. Each initially appeared as **Only me** with **Content under review**; both later showed **Everyone** after review completed. Do not change privacy or upload another copy merely because a submitted post is still under review.

## Repeatable verification

1. Reuse the requested source edit, complete intro and timed burned lyrics. Keep its duration and file hash with the private release plan.
2. Prepare a platform-length caption with source attribution and the pinned public recipe. The observed limits were 2,200 Instagram caption characters and 4,000 TikTok description characters; recheck the actual platform and installed helper before another release.
3. Verify the intended brand account. Create one durable receipt before upload and keep its resulting post URL even if later checks fail.
4. Enable and verify the available native disclosure controls. Record any unsupported control accurately.
5. Reconcile existing drafts and uncertain receipts before retrying. An assigned post URL means verification should continue against that post, rather than starting a new upload.
6. Read back the published owner, caption and recipe link. TikTok's displayed description normalizes whitespace, so compare its normalized text while retaining the original caption file.
7. Verify public visibility after review, playable duration/audio and the displayed disclosure when available. Share the complete verified batch once with the privately configured authorized destination.

Keep authentication files, platform session state, private sharing identifiers and provider receipts outside this public repository.
