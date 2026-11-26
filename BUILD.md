# BUILD note — news-image-20261125

- Built: 26 Nov 2026, 10:21-10:24 WIB, sandbox only.
- Generator: fresh `main.py` (Pillow, DejaVu fonts, no network), written
  in the same layout pattern as the 22 Nov entry (masthead, region bar,
  UTC timeline, 3 illustrated leads, 8 illustrated secondaries,
  24 numbered briefs, DATE CHECK box). The old generator in the trash
  was read for reference only; it was not copied, imported or executed.
- Render: `entry.png` 1024x1024, 185,706 bytes, sha256
  0ffcc0efbe3314513bdb9e421fc478a6e417e4c178446f408814c41301456a33.
  Deterministic: run twice, identical bytes (cmp clean).
- Region counts asserted in code: ASIA 7, EUROPE 10, AMERICAS 8,
  AFRICA 2, MIDDLE EAST 4, OCEANIA 1, GLOBAL 3 = 35 stories.
- Fixes during the build (visual check of the render): timeline strip
  moved down 8px so the region bar no longer overlaps "THE DAY IN UTC";
  8 secondary summaries shortened to fit one line; 2 briefs shortened
  (Geneva, Phnom Penh); 6 illustration labels moved clear of drawings
  (Shenzhou smoke, refinery flame, Odesa flash, Sudan drone, Solomons
  palm, Nvidia chip, tariffs cranes).
- Problems: none blocking. Two hedges (see README): Hormuz tanker count
  differs across sources (2/3/4), so no count is stated; Champions
  League day-one results are 24 Nov, only the UEFA Wednesday-night set
  is used. One item could not be used: "India backs flood-hit Nepal"
  (truncated search snippet, could not verify) — left out.
- NOT submitted. No repo created, no wallet, no signature, no payment.
  Next step for the parent: create the public GitHub repo and submit
  via make.fun before Fri 27 Nov 2026 07:00 WIB (max 5 entries/day cap
  applies across all make.fun entries).
