# Oakencode Bible — Text Sources & Provenance

All texts are public domain or free-licensed. Normalized 2026-10-21 into one
verse-keyed JSON format (book/chapter/verse), chunked per book, by
`normalize.py` (build workspace). Data lives in this folder:
`kjv/`, `web/`, `brenton/`, `wlc/`, plus `books.json` (canon metadata and
the 54 parashiyot).

## King James Version (`kjv/`, 66 books)
- Text: King James Version (1611). **Public domain.**
- Dataset: JSON edition from the open-source `thiagobodruk/bible` project
  (https://github.com/thiagobodruk/bible, file `json/en_kjv.json`).
- Spot-verified: Gen 1:1, John 1:1, Rev 22:21, Ps 119 = 176 verses.

## World English Bible (`web/`, 66 books)
- Text: World English Bible — a modern English translation made from the
  Greek Majority Text and the Hebrew Masoretic Text. **Public domain**
  (the WEB is deliberately released into the public domain by its
  publishers).
- Source: eBible.org (https://ebible.org), USFM download
  `eng-web_usfm.zip` (https://ebible.org/Scriptures/eng-web_usfm.zip).
  Footnotes and cross-references stripped in normalization; verse text kept.
- Note: eBible's WEB also ships deuterocanonical books; v1 includes the
  66-book canon so it navigates in parallel with the KJV.

## Brenton's Septuagint (`brenton/`, 39 OT books)
- Text: *The Septuagint Version of the Old Testament*, English translation
  by Sir Lancelot Charles Lee Brenton (1844). **Public domain.**
- Source: eBible.org, USFM download `eng-Brenton_usfm.zip`
  (https://ebible.org/Scriptures/eng-Brenton_usfm.zip). Footnotes stripped.
- eBible files Daniel under the Greek book code DAG and Esther under ESG;
  both are included here as Daniel and Esther. Deuterocanonical books
  (Tobit, Judith, Wisdom, Sirach, Maccabees, etc.) are present in the
  source but deferred in v1.
- Spot-verified: Gen 1:1 "In the beginning God made the heaven and the
  earth."

## Hebrew Torah (`wlc/`, 5 books)
- Text: Westminster Leningrad Codex (WLC) — the complete pointed Masoretic
  text, based on the Leningrad Codex. **Public domain** (the codex text;
  Tanach.us distributes the WLC as a public-domain edition).
- Source: Tanach.us (https://www.tanach.us), per-book XML:
  `https://www.tanach.us/Books/<Book>.xml` for Genesis–Deuteronomy.
- Treatment: vowel points kept; cantillation accents, meteg and paseq
  removed for a clean reading text; where a verse has a ketiv/qere pair,
  the qere (the read form) is used. Sof pasuq (verse end) retained.

## Parashiyot (weekly Torah portions, in `books.json`)
- The 54 portions with their full-reading verse ranges (aliyah 1 start to
  aliyah 7 end) from the Hebcal leyning data (`aliyot.json`,
  https://github.com/hebcal/hebcal-leyning). Hebcal data is free to use
  with attribution; the live "This Week's Torah Portion" card also queries
  the Hebcal calendar API in the reader's browser and attributes Hebcal.

## Versification note (parallel view)
- KJV and WEB follow Masoretic numbering. Brenton follows the Septuagint,
  whose Psalm numbering differs (e.g. MT Psalms 9+10 = LXX Psalm 9;
  LXX has 151 psalms). The reader maps Psalm chapters between the two
  traditions so the same psalm appears in both columns, and displays a
  note when it does. Verse counts inside a matched chapter can still
  differ slightly. Other LXX/MT divergences (notably Jeremiah's chapter
  order in the Greek) are not remapped in v1: the parallel view is
  verse-keyed within same-numbered chapters, and a chapter that exists in
  only one tradition shows an em dash in the other column.
