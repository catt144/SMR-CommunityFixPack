# C92 public authoring evidence

Read 2026-09-13, repository HEAD `ccd4ff5`. These are publisher/designer statements,
not measurements of the installed game. No public message was sent.

**SOURCE — July 14, 2026, senior designer's research diary.** Cluster numbers primarily
help players locate technologies; they do not specify a required research order.
Higher numbers tend to be farther from the origin. The board intentionally leaves
space for future technologies, fields and connections. Technology cost depends on
when the player earns/spends points, not a fixed price tied to a node's distance.
This constrains the old-tier mapping and empty-slot hypotheses: neither numbered
clusters nor open board space independently establish a missing technology.
[Haemimont Diaries #4: Lab Leaks](https://steamcommunity.com/games/3215050/announcements/detail/699895897307217965).

**SOURCE — July 28, 2026, political design diary.** Laws were being changed to offer
tradeoffs rather than function as another research progression. This supports the
general law-to-tech transition context; it does not name Underground Exploitation,
choose its position, or establish whether its unfinished state was deliberate.
[Haemimont Diaries #5: Political Decisions](https://steamcommunity.com/games/3215050/announcements/detail/667245886315695231).

**SOURCE — September 8, 2026, release announcement.** The publisher identifies the new
research board as part of the free Services & Science update.
[Feeding the Future release announcement](https://www.paradoxinteractive.com/games/surviving-mars-relaunched/news/surviving-mars-relaunched-feeding-the-future-is-out-now).

**MEASURED retrieval route.** The browser's single-event Steam pages exposed almost no
body text. The public Steam News API returned the complete publisher-authored BBCode
for both diary titles, including screenshot paths. Reproduce using Python's
`json.load(urllib.request.urlopen(url))` at
`https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3215050&count=100&maxlength=0`,
then select `appnews.newsitems` by the two titles above. API timestamps were
`1784038280` and `1785247391`; external-post identifiers were `1837955055366232`
and `1839041357038396`, respectively. This read is independent of the installed
game's Steam build `24995074`.

**INFERRED limit.** The opened material contains no explicit placement instruction or
asset assignment for Underground Exploitation. This is a bounded reading, not a
claim that no developer ever published one. The research diary's screenshots were
passed to the placement investigation for visual comparison.
