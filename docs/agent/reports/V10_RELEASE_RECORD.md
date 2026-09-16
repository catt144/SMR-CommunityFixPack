# V10 release and deployment record

Historical record recovered from STATE at
`19c695473474faafec194b55553646e60496a7d9`, before its admission cleanup.
The passages below are exact transcriptions of dated receipts and then-current
release context. They are not a new inspection of Steam, Paradox, the website
or the adjacent repositories. ?Live,? ?uncommitted? and prediction values
retain their original dates and scope.

## Release and delivered artifact

> - ⭐ **v10 IS LIVE on both portals** (2026-09-13, owner's word): `pdx_id` **156049**, `steam_id` **3787202810**,
>   tree `version` **11**, `pdx_version` "9", count word **Forty-nine**. C85 + C89 + C88 in, F37/F43+F118/F31 out.
> - Shipping artifact: Steam-delivered `ModContent.fpk` **371,327 B** md5 `bef42a2d5405e06444b7e6efdf28cf38`
>   (workshop folder, 09-13 00:25 local). Pack-size predictor: `tools/pack_predict.py`.
>   ✅ The "56 vs 54" gap was a READER DEFECT, not a packaging one: `flpk_extract` re-read nested tables under the
>   parent prefix and double-counted two entries (`reports/DOC_OVERHAUL_AUDIT.md` §1). v10 shipped **54**, matching
>   the prediction exactly. Fixed + gated by doccheck's FLPK SELFTEST; `*/.agents/*` now pack-ignored, model **52**.
>   PDX size unread; the two portals' sizes differed on v5/v6 (`RELEASE_PORTAL_PREP` §0.5(f)).

The artifact measurement and reader-defect explanation have their evidence in
[DOC_OVERHAUL_AUDIT ?1](DOC_OVERHAUL_AUDIT.md#1-confirmed-instrument-correctness-was-missing-from-the-overhauls-scope).
The release ledger's ?Released in v10? record is
`docs/agent/prompts/perma/RELEASE_OUTBOX.md`. Its older unexplained-extra-entry
wording predates the reader correction recorded above. The pack predictor and
FLPK SELFTEST compute/check the corresponding current data.

## Release history and field-evidence limit

> - Post-launch LIVE: F105, F107, F108 (v4), F110 (v5), hotfix 2 (v6), C74+C77+C83 (v7), F119+C86 (v8), F59 repair +
>   F60 out (v9), C85+C89+C88 in / F37+F43+F118+F31 out (v10); F104 NOT OURS. ⛔ F107 field route untested.

F107's entry, ?What this leg still does NOT establish,? preserves the untested
field route; F104's entry preserves the not-ours attribution. These release
receipts do not upgrade either evidence claim.

## Site receipt and owner-controlled publication

> - ✅ SITE DEPLOYED 2026-09-13 07:06Z, `d86a347`, state `success` (deployments API + live page read): **49** live rows
>   (45 success + 4 question) = the card's Forty-nine, first agreement since 09-11. Live FAQ carries "Four judgment calls"
>   and no longer promises the retired farm-oxygen repair. ⚖️ The deploy is the owner's act; `publish-site.yml` is
>   `workflow_dispatch` only. Live-deployment read route: `agent/support/LIVE_SITE_READ.md`.
>   Owner's 2 pared files (`for-modders.md`, `install.md`) stay uncommitted = decision 47.

The continuing publication boundary and live-read method are in
`docs/agent/support/LIVE_SITE_READ.md`. Checklist 47 remains the source for the
owner's wording decision; this transfer does not settle it or claim those
adjacent files are still dirty today.
