#!/usr/bin/env python3
"""Build the Oakencode /apps/ static section from approved copy.
Run: python3 build.py   -> outputs into ./site/
"""
import os, shutil
from decimal import Decimal, ROUND_HALF_UP

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")
ASSETS_SRC = {
    "/home/hatch/workspace/pers-int-icons/playstore.png": "assets/img/pers-int-icon.png",
    "/home/hatch/workspace/plant-care-assets/plant-care-icon-512.png": "assets/img/plant-care-icon.png",
    "/home/hatch/workspace/plant-care-assets/plant-care-feature-graphic-1024x500.png": "assets/img/plant-care-feature-graphic.png",
    "/home/hatch/workspace/plant-care-assets/plant-care-hero.png": "assets/img/plant-care-hero.png",
    "/home/hatch/workspace/plant-care-assets/screenshots-final/01-plant-list.png": "assets/img/plant-care-shot-list.png",
    "/home/hatch/workspace/plant-care-assets/screenshots-final/02-plant-detail.png": "assets/img/plant-care-shot-detail.png",
    "/home/hatch/workspace/plant-care-assets/screenshots-final/03-template-picker.png": "assets/img/plant-care-shot-picker.png",
    "/home/hatch/workspace/plant-care-assets/screenshots-final/04-add-plant.png": "assets/img/plant-care-shot-add.png",
    "/home/hatch/workspace/plant-care-assets/screenshots-final/05-settings.png": "assets/img/plant-care-shot-settings.png",
    "/home/hatch/workspace/oakencode-website/assets-src/plant-care-moxie-ad-web.png": "assets/img/plant-care-shot-moxie.png",
    "/home/hatch/workspace/pet-health-vault-assets/pet-health-vault-icon-512.png": "assets/img/pet-health-vault-icon.png",
    "/home/hatch/workspace/private-diary-assets/private-diary-icon-512.png": "assets/img/private-diary-icon.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/01-pet-list.png": "assets/img/pet-health-vault-shot-list.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/02-pet-detail.png": "assets/img/pet-health-vault-shot-detail.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/03-breed-picker.png": "assets/img/pet-health-vault-shot-picker.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/04-edit-pet.png": "assets/img/pet-health-vault-shot-edit.png",
    "/home/hatch/workspace/oakencode-website/assets-src/pet-health-vault-moxie-ad-web.png": "assets/img/pet-health-vault-shot-moxie.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/06-allergies-alert.png": "assets/img/pet-health-vault-shot-allergies.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/07-sitter-handoff.png": "assets/img/pet-health-vault-shot-sitter.png",
    "/home/hatch/workspace/pet-health-vault-assets/screenshots-final/08-pet-id-card.png": "assets/img/pet-health-vault-shot-idcard.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-pet-presenter.png": "assets/img/moxie-pet-presenter.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-hero.png": "assets/img/moxie-hero.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder.png": "assets/img/maestrr-founder.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder-hat.png": "assets/img/maestrr-founder-hat.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder-hat-full.png": "assets/img/maestrr-founder-hat-full.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder-tie.png": "assets/img/maestrr-founder-tie.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder-mandarin.png": "assets/img/maestrr-founder-mandarin.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder-tie-full.png": "assets/img/maestrr-founder-tie-full.png",
    "/home/hatch/workspace/oakencode-website/assets-src/maestrr-founder-mandarin-full.png": "assets/img/maestrr-founder-mandarin-full.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-persint-presenter.png": "assets/img/moxie-persint-presenter.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-plant-presenter.png": "assets/img/moxie-plant-presenter.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-home-cohort.png": "assets/img/moxie-home-cohort.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-index-a.png": "assets/img/moxie-index-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-index-b.png": "assets/img/moxie-index-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-persint-a.png": "assets/img/moxie-persint-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-persint-b.png": "assets/img/moxie-persint-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-plant-strip.png": "assets/img/moxie-plant-strip.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-pet-strip.png": "assets/img/moxie-pet-strip.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-diary-a.png": "assets/img/moxie-diary-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-diary-b.png": "assets/img/moxie-diary-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-budget-a.png": "assets/img/moxie-budget-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-budget-b.png": "assets/img/moxie-budget-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-car-a.png": "assets/img/moxie-car-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-car-b.png": "assets/img/moxie-car-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-gym-a.png": "assets/img/moxie-gym-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-gym-b.png": "assets/img/moxie-gym-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-bill-a.png": "assets/img/moxie-bill-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-bill-b.png": "assets/img/moxie-bill-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-baby-a.png": "assets/img/moxie-baby-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-baby-b.png": "assets/img/moxie-baby-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-collection-a.png": "assets/img/moxie-collection-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-collection-b.png": "assets/img/moxie-collection-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-privacy-a.png": "assets/img/moxie-privacy-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-privacy-b.png": "assets/img/moxie-privacy-b.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-support-a.png": "assets/img/moxie-support-a.png",
    "/home/hatch/workspace/oakencode-website/assets-src/moxie-support-b.png": "assets/img/moxie-support-b.png",
}

CSS = """\
:root {
  --bg: #0a0e1a;
  --bg2: #101828;
  --gold: #d4af37;
  --gold-dim: #9a7d24;
  --text: #e8e6df;
  --muted: #a8a49a;
  --card: #131c2e;
  --line: #2a3450;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
img { max-width: 100%; height: auto; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  padding: 0 1.25rem 4rem;
}
.wrap { max-width: 960px; margin: 0 auto; }
header.site {
  padding: 1.5rem 0;
  border-bottom: 1px solid var(--line);
  margin-bottom: 2.5rem;
  display: flex; align-items: center; justify-content: space-between;
}
.brand { color: var(--gold); font-weight: 700; font-size: 1.25rem; text-decoration: none; letter-spacing: .04em; }
nav a { color: var(--muted); text-decoration: none; margin-left: 1.25rem; font-size: .95rem; }
nav a:hover { color: var(--gold); }
.hero { text-align: center; padding: 2.5rem 0 1rem; }
.hero h1 { font-size: 2rem; color: var(--gold); margin-bottom: .75rem; line-height: 1.25; }
.hero p { color: var(--muted); max-width: 620px; margin: 0 auto; }
.grid {
  display: grid; gap: 1.25rem; margin-top: 2.5rem;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
}
.card {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 1.5rem;
  text-decoration: none; color: var(--text);
  display: flex; flex-direction: column; gap: .6rem;
  transition: border-color .15s;
}
.card:hover { border-color: var(--gold); }
.card .icon { width: 64px; height: 64px; border-radius: 14px; }
.card .mono {
  width: 64px; height: 64px; border-radius: 14px;
  background: #0d1424; border: 1px solid var(--gold-dim);
  color: var(--gold); font-size: 1.75rem; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.card h2 { font-size: 1.15rem; }
.card p { color: var(--muted); font-size: .95rem; flex: 1; }
.badge {
  display: inline-block; font-size: .75rem; font-weight: 600;
  text-transform: uppercase; letter-spacing: .06em;
  padding: .2rem .6rem; border-radius: 999px;
  border: 1px solid var(--gold-dim); color: var(--gold);
  align-self: flex-start;
}
.badge.testing { border-color: #4da3ff; color: #4da3ff; }
.badge.dev { border-color: #b48cff; color: #b48cff; }
.teaser {
  margin-top: 3rem; padding: 1.5rem;
  border: 1px dashed var(--line); border-radius: 12px;
  color: var(--muted); font-size: .95rem;
}
.teaser strong { color: var(--gold); }
.sub-hero { text-align: center; padding: 1.5rem 0 2rem; }
.sub-hero img.icon-lg { width: 120px; height: 120px; border-radius: 26px; margin-bottom: 1rem; }
.sub-hero img.banner { width: 100%; max-height: 280px; object-fit: cover; border-radius: 12px; margin-bottom: 1.25rem; }
.sub-hero h1 { font-size: 1.9rem; margin-bottom: .5rem; }
.sub-hero .tagline { color: var(--muted); font-size: 1.1rem; margin-bottom: .75rem; }
section.block { margin: 2rem 0; }
section.block h2 { color: var(--gold); font-size: 1.15rem; margin-bottom: .75rem; text-transform: uppercase; letter-spacing: .05em; font-size: .95rem; }
ul.feat { list-style: none; }
ul.feat li { padding: .45rem 0 .45rem 1.5rem; position: relative; }
ul.feat li::before { content: "◆"; color: var(--gold-dim); position: absolute; left: 0; font-size: .8rem; }
.shots {
  display: grid; gap: 1.25rem; margin-top: 1.25rem;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}
.shots figure { margin: 0; text-align: center; }
.shots img {
  width: 100%; border-radius: 12px; border: 1px solid var(--line);
  display: block;
}
.shots figcaption { color: var(--muted); font-size: .9rem; margin-top: .5rem; }
.privacy {
  background: var(--bg2); border: 1px solid var(--line);
  border-radius: 12px; padding: 1.25rem 1.5rem; margin-top: 2.5rem;
  color: var(--muted); font-size: .95rem;
}
.privacy strong { color: var(--gold); }
.cta { margin-top: 2rem; text-align: center; }
.btn {
  display: inline-block; background: var(--gold); color: #0a0e1a;
  font-weight: 700; padding: .8rem 1.75rem; border-radius: 999px;
  text-decoration: none;
}
.btn:hover { filter: brightness(1.1); }
.back { display: inline-block; margin-top: 2.5rem; color: var(--muted); text-decoration: none; }
.back:hover { color: var(--gold); }
.hero .hero-model { width: 100%; max-width: 420px; border-radius: 16px; border: 1px solid var(--line); margin: 1.5rem auto; display: block; }
.btn-ghost { background: transparent; color: var(--gold); border: 1px solid var(--gold-dim); margin-left: .75rem; }
.app-section { display: flex; gap: 2rem; align-items: center; margin: 3rem 0; }
.app-section.flip { flex-direction: row-reverse; }
.app-media { flex: 0 0 280px; }
.app-media img { width: 100%; border-radius: 12px; border: 1px solid var(--line); display: block; }
.app-body { flex: 1; }
.app-body .icon { width: 96px; height: 96px; border-radius: 22px; display: block; margin-bottom: .5rem; }
.app-body h2 { font-size: 1.5rem; margin: .5rem 0 .25rem; }
.app-body .tagline { color: var(--muted); margin-bottom: .75rem; }
.app-body .dl-note { color: var(--muted); font-size: .85rem; margin-top: .75rem; }
.founder { display: flex; gap: 2rem; align-items: flex-start; background: var(--bg2); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem; margin-top: 3rem; }
.founders-row { display: flex; gap: 1.25rem; flex: 0 0 auto; }
.person { flex: 1 1 0; min-width: 0; text-align: center; }
.person img { width: 100%; max-width: 180px; border-radius: 12px; border: 1px solid var(--line); display: block; margin: 0 auto; }
.person h3 { margin: .7rem 0 .3rem; font-size: 1rem; color: var(--gold); }
.strip { display: grid; gap: 1rem; margin-top: 1.5rem; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
.strip .card { padding: 1rem; }
.strip .card h2 { font-size: 1rem; }
.strip .card p { font-size: .85rem; }
@media (max-width: 720px) { .app-section, .app-section.flip, .founder { flex-direction: column; } .app-media { flex: none; max-width: 280px; } }
footer { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .85rem; text-align: center; }
footer a { color: var(--gold); }
.credits { margin-top: .9rem; line-height: 1.55; }
.lab { color: var(--muted); font-size: .85rem; }
section.block.lab h2 { color: var(--muted); font-size: .8rem; }
.lab p { margin: .4rem 0; }
.lab strong { color: var(--text); }
.amount-box { background: var(--bg2); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem; margin-top: 2rem; text-align: center; }
.amount-box h2 { color: var(--gold); font-size: 1rem; text-transform: uppercase; letter-spacing: .05em; margin-bottom: 1rem; }
.chips { display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; margin-bottom: 1rem; }
.chip { background: var(--card); color: var(--text); border: 1px solid var(--line); border-radius: 999px; padding: .5rem 1.1rem; font-size: 1rem; cursor: pointer; font-family: inherit; }
.chip:hover { border-color: var(--gold); }
.chip.active { background: var(--gold); color: #0a0e1a; font-weight: 700; border-color: var(--gold); }
.custom-amount { color: var(--muted); font-size: .95rem; }
.custom-amount input { width: 110px; background: var(--card); border: 1px solid var(--line); border-radius: 8px; color: var(--text); padding: .5rem .6rem; font-size: 1rem; text-align: center; font-family: inherit; }
.custom-amount input:focus { outline: none; border-color: var(--gold); }
.legal { border-top: 1px solid var(--gold-dim); border-bottom: 1px solid var(--gold-dim); color: var(--muted); font-size: .92rem; text-align: center; padding: 1rem .5rem; margin: 2rem 0; }
.methods { display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); }
.method-card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 1.5rem; display: flex; flex-direction: column; gap: .7rem; }
.method-card h2 { font-size: 1.2rem; color: var(--gold); }
.method-card .handle { color: var(--muted); font-size: .95rem; }
.method-card .handle strong { color: var(--text); }
.method-card .note { color: var(--muted); font-size: .88rem; }
.figs { border-top: 1px solid var(--line); padding-top: .7rem; }
.figs .row { display: flex; justify-content: space-between; padding: .25rem 0; color: var(--muted); }
.figs .row strong { color: var(--text); }
.figs .row.total strong { color: var(--gold); }
.method-card .btn { text-align: center; margin-top: auto; }
.on-the-way { text-align: center; color: var(--muted); margin-top: 2rem; }
.fee-note { text-align: center; color: var(--muted); font-size: .85rem; margin-top: .75rem; }
"""

PLANT_APK = "https://github.com/Jamesthesailor/oakencode-website/releases/download/apk-v1.0.0/plant-care.apk"
PET_APK = "https://github.com/Jamesthesailor/oakencode-website/releases/download/apk-v1.0.0/pet-health-vault.apk"
DIARY_APK = "https://github.com/Jamesthesailor/oakencode-website/releases/download/apk-v1.0.0/private-diary.apk"
PERSINT_TESTER = "https://play.google.com/apps/testing/com.persint.app"
PLAY_NOTE = "Google Play is still reviewing our developer access — download the app here today; the Play version is coming."

APPS = [
    dict(slug="pers-int", name="Pers-int", status="In closed testing", badge="testing",
         tag="Your personal intelligence app — see what the internet knows about you.",
         icon="pers-int-icon.png", mono=None, hero_img=None,
         desc="Your personal intelligence app — see what the internet knows about you.",
         feats=[
             "Photo EXIF check: find hidden GPS location data before you share",
             "Username search across 1,000+ sites",
             "Email and password breach checks",
             "Family dossier — findings for the people you care about, stored only on your phone",
         ],
         pricing=None,
         cta=("Become a tester", "https://play.google.com/apps/testing/com.persint.app"),
         founder="maestrr-founder.png", strip=["moxie-persint-a.png", "moxie-persint-b.png"]),
    dict(slug="plant-care", name="Plant Care", status="Available now", badge="",
         tag="Your plants, on a schedule.",
         icon="plant-care-icon.png", mono=None, hero_img="plant-care-feature-graphic.png",
         desc="Plant Care is your pocket plant keeper — for people who love plants but forget to water them.",
         feats=[
             "Water & feed reminders at 9am; due and overdue at a glance",
             "Photo timeline per plant; care history logged automatically",
             "103 common-plant templates — Snake Plant, Pothos, Monstera, Basil, Tomato, Strawberry, and more",
             "Backup, export, import — your data is yours",
         ],
         pricing="Free for up to 5 plants. One-time $4.99 Pro unlock for unlimited plants.",
         shots=[
             ("plant-care-shot-list.png", "Your plants, on a schedule."),
             ("plant-care-shot-detail.png", "Water, feed, done."),
             ("plant-care-shot-picker.png", "103 common plants, preloaded."),
             ("plant-care-shot-add.png", "Set up in seconds."),
             ("plant-care-shot-settings.png", "Private by design."),
             ("plant-care-shot-moxie.png", "Moxie presents Plant Care."),
         ],
         cta=("Download APK", PLANT_APK),
         note=PLAY_NOTE,
         founder="maestrr-founder-mandarin.png", strip=["moxie-plant-strip.png"]),
    dict(slug="pet-health-vault", name="Pet Health Vault", status="Available now", badge="",
         tag="Your pet's whole health story — scheduler, diary, logs, and vault. Offline, private, yours.",
         icon="pet-health-vault-icon.png", mono="P", hero_img=None,
         desc="Pet Health Vault keeps your pet's whole health story in one private place — and it never leaves your phone.",
         feats=[
             "Reminders for vaccinations, vet visits, and meds — with a multi-pet calendar",
             "Health diary, weight tracker with trend chart, and feed / water / walk logs",
             "57 breed templates with sensible care guidance",
             "Allergies on every profile — shown as an alert right on the pet's page",
             "Owner & emergency contacts, printed on the pet ID card and sitter sheet",
             "The PDF kit: health reports, vaccination certificates, pet ID card, sitter handoff sheet, ZIP export",
             "Freedom Units by default (pounds, ounces, miles); metric optional",
             "Documents vault, photo gallery, backup and export — your data never leaves your phone",
         ],
         pricing="Free for up to 3 pets — calendar and bulk actions included. One-time $4.99 Pro unlock in the Play version: unlimited pets, CSV export, and the PDF kit — vet-visit health reports, vaccination certificates, a printable pet ID & emergency card, a sitter handoff sheet, and full ZIP export.",
         shots=[
             ("pet-health-vault-shot-list.png", "Every pet, at a glance."),
             ("pet-health-vault-shot-detail.png", "Health, logs, and records in one place."),
             ("pet-health-vault-shot-picker.png", "57 breeds with care guidance."),
             ("pet-health-vault-shot-edit.png", "Set up in seconds."),
             ("pet-health-vault-shot-allergies.png", "Allergies, front and center."),
             ("pet-health-vault-shot-sitter.png", "A handoff sheet for the sitter."),
             ("pet-health-vault-shot-idcard.png", "A pet ID card for wallet or fridge."),
             ("pet-health-vault-shot-moxie.png", "Moxie presents Pet Health Vault."),
         ],
         cta=("Download APK", PET_APK),
         note=PLAY_NOTE,
         founder="maestrr-founder-tie-full.png", strip=["moxie-pet-strip.png"]),
    dict(slug="private-diary", name="Private Diary", status="Available now", badge="",
         tag="A locked, encrypted diary. PIN unlock, on-device only, no ads, no accounts.",
         icon=None, mono="D", hero_img=None,
         desc="Your diary should be yours. Not a company's, not a cloud's, not anyone's. Private Diary keeps every entry on your phone, encrypted, behind a PIN. No account. No sign-up. No ads. Nothing to sync because there's nothing to leak — we couldn't read your diary if we wanted to.",
         feats=[
             "PIN lock — it re-locks the moment you leave the app",
             "Every entry encrypted on the device (AES-256)",
             "Unlimited entries in your first notebook",
             "Calendar view, full-text search, tags and mood markers",
             "Seven themes, including the Oakencode navy & gold",
             "Backup export and import — free, always. Your backup is free. Your words are yours.",
         ],
         pricing="Free for one notebook — unlimited entries, calendar, search, tags, moods, and backup export included; the lock and the encryption are never paywalled. One-time $4.99 Pro unlock in the Play version: multiple notebooks, photo attachments in entries, sealed time-capsule entries that won't open until a date you choose, a print-ready PDF journal book, and a decoy notebook with its own duress PIN.",
         cta=("Download APK", DIARY_APK),
         note=PLAY_NOTE,
         founder="maestrr-founder-hat-full.png", strip=["moxie-diary-a.png", "moxie-diary-b.png"]),
    dict(slug="budget-tracker", name="Budget Tracker", status="Planned", badge="",
         tag="Manual money tracking, offline. Your money, your phone.",
         icon=None, mono="B", hero_img=None,
         desc="Manual money tracking, offline. Your money, your phone.",
         feats=[
             "Envelopes and categories you define — no bank linking, ever",
             "Spending log with running totals",
             "Simple charts of where it went",
             "Export CSV",
         ],
         pricing=None, cta=None,
         founder="maestrr-founder-mandarin-full.png", strip=["moxie-budget-a.png", "moxie-budget-b.png"]),
    dict(slug="car-log", name="Car Log", status="Planned", badge="",
         tag="Fuel, service, repairs — your car's whole history.",
         icon=None, mono="C", hero_img=None,
         desc="Fuel, service, repairs — your car's whole history.",
         feats=[
             "Fuel fill-ups with MPG tracking",
             "Service and repair log with receipt photos",
             "Reminders for oil, tires, inspections",
             "Cost-per-mile over time",
         ],
         pricing=None, cta=None,
         founder="maestrr-founder-tie.png", strip=["moxie-car-a.png", "moxie-car-b.png"]),
    dict(slug="gym-tracker", name="Gym Tracker", status="Planned", badge="",
         tag="Log workouts offline. No account, no cloud.",
         icon=None, mono="G", hero_img=None,
         desc="Log workouts offline. No account, no cloud.",
         feats=[
             "Routines, sets, reps, weights",
             "Progress graphs that don't hide behind a paywall",
             "Rest timer",
             "Export your data",
         ],
         pricing=None, cta=None,
         founder="maestrr-founder.png", strip=["moxie-gym-a.png", "moxie-gym-b.png"]),
    dict(slug="bill-splitter", name="Bill Splitter", status="Planned", badge="",
         tag="Split bills with friends. No accounts, no fees.",
         icon=None, mono="S", hero_img=None,
         desc="Split bills with friends. No accounts, no fees.",
         feats=[
             "Split evenly, by shares, or by item",
             "Running balances per group",
             "Settle-up tracking",
             "Works fully offline — no sign-up for anyone",
         ],
         pricing=None, cta=None,
         founder="maestrr-founder-mandarin.png", strip=["moxie-bill-a.png", "moxie-bill-b.png"]),
    dict(slug="baby-log", name="Baby Log", status="Planned", badge="",
         tag="Feeds, sleep, diapers, milestones — for tired parents, offline.",
         icon=None, mono="B", hero_img=None,
         desc="Feeds, sleep, diapers, milestones — for tired parents, offline.",
         feats=[
             "One-tap logging for feeds, sleep, diapers",
             "Growth and milestone tracking",
             "Patterns over days and weeks",
             "Private — no cloud nursery",
         ],
         pricing=None, cta=None,
         founder="maestrr-founder-tie-full.png", strip=["moxie-baby-a.png", "moxie-baby-b.png"]),
    dict(slug="collection-vault", name="Collection Vault", status="Planned", badge="",
         tag="Catalog any collection. Barcode, photo, inventory — offline.",
         icon=None, mono="C", hero_img=None,
         desc="Catalog any collection. Barcode, photo, inventory — offline.",
         feats=[
             "Barcode scan plus photo per item",
             "Custom fields per collection type",
             "Value tracking",
             "Exportable inventory",
         ],
         pricing=None, cta=None,
         founder="maestrr-founder-hat.png", strip=["moxie-collection-a.png", "moxie-collection-b.png"]),
]

TEASER = ("an all-in-one kitchen companion, a document vault, a receipt "
         "vault, a voice recorder, a PDF toolkit, a photo gallery done right, and a video "
         "compressor. Details when they're real — we don't announce vapor.")

# ---------------------------------------------------------------- homepage
PROJECTS = [
    dict(name="Pers-int", status="In closed testing", badge="testing",
         desc="Your personal intel app. Scan usernames across 1,000+ sites, check emails against breach databases, and find GPS data hiding in your photos. Family safety, done right.",
         link="/apps/pers-int/"),
    dict(name="Sovereign", status="In development", badge="dev",
         desc="An agentic investigation platform — the next evolution of field-ready OSINT tooling. Built phone-first, for professionals who work where the case takes them.",
         link=None),
    dict(name="HUMANITIES", status="In development", badge="dev",
         desc="Our persona engine — the durable foundation behind everything we build. One engine, many products. The Unreal Engine of virtual personalities.",
         link=None),
    dict(name="Kindred", status="On the roadmap", badge="",
         desc="Companionship, done honestly. A warm, present conversational partner built on the HUMANITIES engine.",
         link=None),
    dict(name="Nocturne", status="On the roadmap", badge="",
         desc="For adults who want unfiltered conversation. Same engine, no guardrails beyond the law.",
         link=None),
    dict(name="Ogma-TUI", status="On the roadmap", badge="",
         desc="Mobile-first, person-focused OSINT in the terminal. For investigators who live on their phones.",
         link=None),
]

BELIEFS = [
    "No ads, ever",
    "No tracking",
    "Your data stays yours",
    "Pay for software, not with yourself",
]

def app_section(icon_src, name, badge_html, tagline, feats, pricing, cta_label, cta_url, note, presenter_src, presenter_alt, flip=False, page_url=None):
    feats_html = "".join(f"<li>{x}</li>" for x in feats)
    pricing_html = f"<p><strong>Pricing:</strong> {pricing}</p>" if pricing else ""
    flip_cls = " flip" if flip else ""
    heading_html = f'<a href="{page_url}" style="color:inherit;text-decoration:none;">{name}</a>' if page_url else name
    return f"""\
<section class="app-section{flip_cls}">
  <div class="app-media"><img src="{presenter_src}" alt="{presenter_alt}" loading="lazy"></div>
  <div class="app-body">
    <img class="icon" src="{icon_src}" alt="{name} icon">
    <h2>{heading_html}</h2>
    {badge_html}
    <p class="tagline">{tagline}</p>
    <ul class="feat">{feats_html}</ul>
    {pricing_html}
    <div class="cta" style="text-align:left;"><a class="btn" href="{cta_url}">{cta_label}</a></div>
    <p class="dl-note">{note}</p>
  </div>
</section>"""

def brand_strip(founder_img, moxie_imgs):
    persons = [f"""\
    <div class="person">
      <img src="/apps/assets/img/{founder_img}" alt="James Bryant, Founder of Oakencode">
      <h3>James Bryant</h3>
      <span class="badge">Founder</span>
    </div>"""]
    for i, img in enumerate(moxie_imgs):
        if i == 0:
            persons.append(f"""\
    <div class="person">
      <img src="/apps/assets/img/{img}" alt="Miss Moxie Linn, Cohort of Oakencode" loading="lazy">
      <h3>Miss Moxie Linn</h3>
      <span class="badge">Cohort</span>
    </div>""")
        else:
            persons.append(f"""\
    <div class="person">
      <img src="/apps/assets/img/{img}" alt="Miss Moxie Linn of Oakencode" loading="lazy">
    </div>""")
    return f"""\
<section class="block founder">
  <div class="founders-row">
{''.join(persons)}
  </div>
</section>"""

def homepage():
    strip = []
    lab = []
    for p in PROJECTS:
        if p["name"] == "Pers-int":
            continue
        if p["name"] in ("HUMANITIES", "Kindred", "Nocturne"):
            lab.append(f"<p><strong>{p['name']}</strong> — {p['status'].lower()}. {p['desc']}</p>")
            continue
        badge = f'<span class="badge {p["badge"]}">{p["status"]}</span>' if p["badge"] else f'<span class="badge">{p["status"]}</span>'
        strip.append(f'<div class="card"><h2>{p["name"]}</h2>{badge}<p>{p["desc"]}</p></div>')
    strip.append(
        '<a class="card" href="/apps/"><h2>More apps</h2><span class="badge dev">Growing</span>'
        "<p>Diary, budget, car, gym, bills, baby, collections — offline-first tools on the workbench. See them all.</p></a>"
    )
    beliefs = "".join(f"<li>{b}</li>" for b in BELIEFS)
    return f"""\
<div class="hero">
  <img src="/assets/img/oakencode-seal.jpg" alt="Oakencode seal" style="width:120px;height:120px;border-radius:50%;">
  <h1>Honest software, built by a normal man, for normal people.</h1>
  <p>No ads. No tracking. No dark patterns. Just tools that do what they say — and three of them are ready to download right now.</p>
  <img class="hero-model" src="/apps/assets/img/moxie-hero.png" alt="Moxie presenting Oakencode">
  <div class="cta"><a class="btn" href="#apps">Get the apps</a> <a class="btn btn-ghost" href="{PERSINT_TESTER}">Become a Pers-int tester</a></div>
</div>
<section class="block" id="apps">
  <h2>Available now</h2>
  {app_section("/apps/assets/img/plant-care-icon.png", "Plant Care", '<span class="badge">Available now</span>',
      "Your plants, on a schedule.",
      ["Water & feed reminders at 9am; due and overdue at a glance",
       "Photo timeline per plant; care history logged automatically",
       "103 common-plant templates — Snake Plant, Pothos, Monstera, Basil, Tomato, Strawberry, and more",
       "Backup, export, import — your data is yours"],
      "Free for up to 5 plants. One-time $4.99 Pro unlock in the Play version.", "Download APK", PLANT_APK, PLAY_NOTE,
      "/apps/assets/img/moxie-plant-presenter.png", "Moxie presenting Plant Care", flip=True)}
  {app_section("/apps/assets/img/pet-health-vault-icon.png", "Pet Health Vault", '<span class="badge">Available now</span>',
      "Your pet's whole health story — scheduler, diary, logs, and vault. Offline, private, yours.",
      ["Reminders for vaccinations, vet visits, and meds — with a multi-pet calendar",
       "Health diary, weight tracker with trend chart, and feed / water / walk logs",
       "57 breed templates with sensible care guidance",
       "Allergies on every profile, plus owner & emergency contacts",
       "Documents vault, photo gallery, backup and export — your data never leaves your phone"],
      "Free for up to 3 pets — calendar and bulk actions included. One-time $4.99 Pro unlock in the Play version: unlimited pets, CSV export, and the PDF kit — vet-visit health reports, vaccination certificates, a printable pet ID & emergency card, a sitter handoff sheet, and full ZIP export.", "Download APK", PET_APK, PLAY_NOTE,
      "/apps/assets/img/moxie-pet-presenter.png", "Moxie presenting Pet Health Vault")}
  {app_section("/apps/assets/img/private-diary-icon.png", "Private Diary", '<span class="badge">Available now</span>',
      "A locked, encrypted diary. PIN unlock, on-device only, no ads, no accounts.",
      ["PIN lock — it re-locks the moment you leave the app",
       "Every entry encrypted on the device (AES-256)",
       "Unlimited entries in your first notebook",
       "Calendar view, full-text search, tags and mood markers",
       "Seven themes, including the Oakencode navy & gold",
       "Backup export and import — free, always. Your backup is free. Your words are yours."],
      "Free for one notebook — unlimited entries, calendar, search, tags, moods, and backup export included; the lock and the encryption are never paywalled. One-time $4.99 Pro unlock in the Play version: multiple notebooks, photo attachments in entries, sealed time-capsule entries that won't open until a date you choose, a print-ready PDF journal book, and a decoy notebook with its own duress PIN.", "Download APK", DIARY_APK, PLAY_NOTE,
      "/apps/assets/img/moxie-diary-a.png", "Moxie presenting Private Diary", flip=True, page_url="/apps/private-diary/")}
</section>
{app_section("/apps/assets/img/pers-int-icon.png", "Pers-int", '<span class="badge testing">In closed testing</span>',
    "Your personal intelligence app — see what the internet knows about you.",
    ["Photo EXIF check: find hidden GPS location data before you share",
     "Username search across 1,000+ sites",
     "Email and password breach checks",
     "Family dossier — findings for the people you care about, stored only on your phone"],
    None, "Become a tester", PERSINT_TESTER,
    "In closed testing on Google Play. Join with the Google account on your phone, then install from the Play Store.",
    "/apps/assets/img/moxie-persint-presenter.png", "Moxie presenting Pers-int", flip=True)}
<section class="block founder">
  <div class="founders-row">
    <div class="person">
      <img src="/apps/assets/img/maestrr-founder-hat.png" alt="James Bryant, Founder of Oakencode">
      <h3>James Bryant</h3>
      <span class="badge">Founder</span>
    </div>
    <div class="person">
      <img src="/apps/assets/img/moxie-home-cohort.png" alt="Miss Moxie Linn, Cohort">
      <h3>Miss Moxie Linn</h3>
      <span class="badge">Cohort</span>
    </div>
  </div>
  <div>
    <h2>The man behind it</h2>
    <p>Oakencode is a one-man shop. James Bryant designs, builds, and ships every app himself — no teams, no ads department. <a href="/support/" style="color:var(--gold);">Our investors are you.</a> Just a normal man making the tools he wanted for his own family, and sharing them with yours.</p>
    <p>Miss Moxie Linn is his cohort — the collaborator behind the scenes and the one who keeps the whole pipeline moving. He builds the apps; she makes sure they ship.</p>
  </div>
</section>
<section class="block">
  <h2>What we believe</h2>
  <p>Most software today treats you as the product. We don't. Oakencode builds tools the way a craftsman builds furniture — to last, to serve, and to respect the person using it.</p>
  <ul class="feat" style="margin-top:1rem;">{beliefs}</ul>
</section>
<section class="block">
  <h2>Also in the works</h2>
  <div class="strip">
  {''.join(strip)}
  </div>
</section>
<section class="block">
  <h2>Get in touch</h2>
  <p>Questions, feedback, or just want to talk shop? We read everything.<br>
  <a href="mailto:contact@oakencode.com" style="color:var(--gold);">contact@oakencode.com</a></p>
</section>
<section class="block lab">
  <h2>From the lab</h2>
  {''.join(lab)}
</section>
"""

# ---------------------------------------------------------------- support
# One dict per support method; the /support/ page renders a card for each, so
# adding a method later means adding one entry here — nothing else changes.
#   fee_pct / fee_flat: the method's published fee (percent + flat USD)
#   url_base + url_suffix: the public link; url_suffix carries an "{amt}"
#     placeholder for the amount-prefilled form ("" if the method has none)
#   handle: the public handle printed on the card for in-app sending
#   Order = what Oakencode keeps, best first (checked at the preset amounts).
SUPPORT_METHODS = [
    dict(name="Venmo", fee_pct=1.9, fee_flat=0.10,
         url_base="https://venmo.com/u/OakenCode", url_suffix="?txn=pay&amount={amt}",
         handle="@OakenCode", button="Support with Venmo"),
    dict(name="Cash App", fee_pct=2.6, fee_flat=0.15,
         url_base="https://cash.app/$OakenCode", url_suffix="/{amt}",
         handle="$OakenCode", button="Support with Cash App"),
    dict(name="Ko-fi", fee_pct=3, fee_flat=0.30,
         url_base="https://ko-fi.com/oakencode", url_suffix="",
         handle="ko-fi.com/oakencode", button="Support on Ko-fi",
         fee_label="Ko-fi takes $0 · PayPal processing (3% + $0.30) takes",
         handle_line="Open <strong>ko-fi.com/oakencode</strong> in your browser, or use the button below."),
    dict(name="PayPal", fee_pct=2.89, fee_flat=0.49,
         url_base="https://www.paypal.com/donate/?hosted_button_id=37JSR7VDHML24", url_suffix="&amount={amt}",
         handle="OakenCode on PayPal", button="Support with PayPal",
         fee_label="PayPal processing (2.89% + $0.49) takes",
         handle_line="Donate to <strong>OakenCode on PayPal</strong> — or just use the button below.",
         note="Donors can add a little to cover the fees — and monthly giving is available."),
]
SUPPORT_DEFAULT_AMOUNT = 10
SUPPORT_PRESETS = (3, 5, 10, 25, 50)

def _money(x):
    return f"${x:,.2f}"

def _support_fee(amount, method):
    fee = (Decimal(str(amount)) * Decimal(str(method["fee_pct"])) / Decimal("100")
           + Decimal(str(method["fee_flat"])))
    return fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def support_page():
    cards = []
    for m in SUPPORT_METHODS:
        amt = SUPPORT_DEFAULT_AMOUNT
        fee = _support_fee(amt, m)
        recv = Decimal(str(amt)) - fee
        href = m["url_base"] + m["url_suffix"].replace("{amt}", f"{amt:g}")
        fee_label = m.get("fee_label", f"{m['name']} takes")
        handle_line = m.get(
            "handle_line",
            f"Send to <strong>{m['handle']}</strong> in the app, or use the button below.")
        note_html = f'\n      <p class="note">{m["note"]}</p>' if m.get("note") else ""
        cards.append(f"""\
    <div class="method-card" data-fee-pct="{m['fee_pct']}" data-fee-flat="{m['fee_flat']}" data-url-base="{m['url_base']}" data-url-suffix="{m['url_suffix']}">
      <h2>{m['name']}</h2>
      <p class="handle">{handle_line}</p>
      <div class="figs">
        <div class="row"><span>You send</span><strong class="f-send">{_money(amt)}</strong></div>
        <div class="row"><span>{fee_label}</span><strong class="f-fee">{_money(fee)}</strong></div>
        <div class="row total"><span>Oakencode receives</span><strong class="f-recv">{_money(recv)}</strong></div>
      </div>{note_html}
      <a class="btn f-btn" href="{href}" target="_blank" rel="noopener">{m['button']}</a>
    </div>""")
    chips = "".join(
        f'<button type="button" class="chip{" active" if a == SUPPORT_DEFAULT_AMOUNT else ""}" data-amount="{a}">${a}</button>'
        for a in SUPPORT_PRESETS
    )
    return f"""\
<div class="hero">
  <h1>Our investors are you.</h1>
  <p>No ads. No trackers. No accounts. Oakencode apps stay free of all three because the people who use them chip in. Pick an amount, see exactly what the payment service takes and what Oakencode receives, then support in one tap — honest math, on both sides.</p>
</div>
<div class="amount-box">
  <h2>Choose an amount (USD)</h2>
  <div class="chips">{chips}</div>
  <label class="custom-amount">Or enter your own: $ <input id="custom-amount" type="number" min="1" step="any" value="{SUPPORT_DEFAULT_AMOUNT}"></label>
</div>
<p class="legal">Oakencode is a for-profit studio, not a charity. Support is not tax-deductible, and it buys no ownership, shares, or returns — it's a tip that keeps the apps free and ad-free.</p>
<div class="methods">
{''.join(cards)}
</div>
<p class="fee-note">Fees as published October 2026; your provider's rates may vary.</p>
{brand_strip("maestrr-founder-tie-full.png", ["moxie-support-a.png", "moxie-support-b.png"])}
<script>
(function () {{
  var input = document.getElementById('custom-amount');
  var chips = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.method-card'));
  function fmt(n) {{ return '$' + n.toFixed(2); }}
  function roundMoney(n) {{ return Math.round((n + 1e-9) * 100) / 100; }}
  function amtForUrl(n) {{ return (Math.round(n * 100) / 100).toString(); }}
  function update() {{
    var amt = parseFloat(input.value);
    if (isNaN(amt) || amt <= 0) {{ return; }}
    chips.forEach(function (c) {{ c.classList.toggle('active', parseFloat(c.getAttribute('data-amount')) === amt); }});
    cards.forEach(function (card) {{
      var pct = parseFloat(card.getAttribute('data-fee-pct'));
      var flat = parseFloat(card.getAttribute('data-fee-flat'));
      var fee = roundMoney(amt * pct / 100 + flat);
      var recv = roundMoney(amt - fee);
      card.querySelector('.f-send').textContent = fmt(amt);
      card.querySelector('.f-fee').textContent = fmt(fee);
      card.querySelector('.f-recv').textContent = fmt(recv);
      var base = card.getAttribute('data-url-base');
      var suffix = card.getAttribute('data-url-suffix');
      card.querySelector('.f-btn').setAttribute('href', suffix ? base + suffix.replace('{{amt}}', amtForUrl(amt)) : base);
    }});
  }}
  chips.forEach(function (c) {{ c.addEventListener('click', function () {{ input.value = c.getAttribute('data-amount'); update(); }}); }});
  input.addEventListener('input', update);
  update();
}})();
</script>
"""

PRIVACY_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Pers-Int Privacy Policy</title>
<style>
body { font-family: -apple-system, sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; line-height: 1.7; color: #222; }
h1 { font-size: 1.8em; }
h2 { margin-top: 1.5em; font-size: 1.2em; }
.updated { color: #666; font-size: 0.9em; }
</style>
</head>
<body>
<h1>Pers-Int Privacy Policy</h1>
<p class="updated">Last updated: October 2026</p>

<p>We collect almost nothing. Here's exactly what happens with your data:</p>

<h2>Your dossiers stay on your device</h2>
<p>Names, emails, usernames, search results — all stored locally in the app on your phone. We never see them, never store them on our servers, never transmit them anywhere.</p>

<h2>Search queries</h2>
<p>When you run a username or email check, your device contacts public websites directly. We do not route these queries through our servers and we do not log them.</p>

<h2>Tokens</h2>
<p>Token purchases are handled by Google Play Billing. We don't see or store your payment information.</p>

<h2>No tracking</h2>
<p>No analytics SDKs. No advertising SDKs. No crash reporting that includes personal data. No ads of any kind — ever.</p>

<h2>What we cannot do</h2>
<p>We cannot share what we do not have. We cannot sell what we never collect. We cannot leak what never leaves your phone.</p>

<h2>Data deletion</h2>
<p>Since all your data is stored only on your device, you can delete it at any time by clearing the app's data or uninstalling the app. There is nothing on our servers to delete because we never receive your data.</p>

<h2>Contact</h2>
<p>Questions about this policy: contact us through the app's About section.</p>

<div style="text-align:center; margin-top:2.5em;">
  <img src="/apps/assets/img/maestrr-founder-mandarin-full.png" alt="James Bryant, Founder of Oakencode" style="width:150px; border-radius:10px; margin:0 6px;">
  <img src="/apps/assets/img/moxie-privacy-a.png" alt="Miss Moxie Linn, Cohort" style="width:150px; border-radius:10px; margin:0 6px;">
  <img src="/apps/assets/img/moxie-privacy-b.png" alt="Miss Moxie Linn, Cohort" style="width:150px; border-radius:10px; margin:0 6px;">
  <p style="color:#666; font-size:0.9em;">James Bryant — Founder &nbsp;·&nbsp; Miss Moxie Linn — Cohort</p>
</div>

<hr>
<footer style="text-align:center; color:#666; font-size:0.9em; margin-top:2em;">
  Oakencode — honest software, built by a normal man, for normal people.<br>
  <a href="mailto:contact@oakencode.com">contact@oakencode.com</a><br>
  <br>
  Owner-Developer: Skipper James Bryant<br>
  Muse-Developer: Miss Moxie Linn<br>
  Credit: Mr. James Allen<br>
  Credit: Miss Amy Hwang
</footer>
</body>
</html>
"""

PRIVACY = "<strong>Privacy first.</strong> No ads, ever. No tracking. No account. Everything stays on your phone."

HEADER = """\
<header class="site">
  <a class="brand" href="https://oakencode.com">Oakencode</a>
  <nav><a href="https://oakencode.com">Home</a><a href="/apps/">Apps</a><a href="/support/">Support</a><a href="mailto:contact@oakencode.com">Contact</a></nav>
</header>"""

FOOTER = """\
<footer>
  Oakencode — honest software, built by a normal man, for normal people.<br>
  <a href="mailto:contact@oakencode.com">contact@oakencode.com</a>
  <div class="credits">
    Owner-Developer: Skipper James Bryant<br>
    Muse-Developer: Miss Moxie Linn<br>
    Credit: Mr. James Allen<br>
    Credit: Miss Amy Hwang
  </div>
</footer>"""

def page(title, body):
    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Oakencode</title>
<link rel="stylesheet" href="/apps/assets/css/style.css">
</head>
<body>
<div class="wrap">
{HEADER}
{body}
{FOOTER}
</div>
</body>
</html>
"""

def icon_html(app, cls):
    if app["icon"]:
        return f'<img class="{cls}" src="/apps/assets/img/{app["icon"]}" alt="{app["name"]} icon">'
    return f'<div class="{cls} mono">{app["mono"]}</div>'

def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "apps", "assets", "css"))
    os.makedirs(os.path.join(OUT, "apps", "assets", "img"))
    os.makedirs(os.path.join(OUT, "assets", "img"))
    with open(os.path.join(OUT, "apps", "assets", "css", "style.css"), "w") as f:
        f.write(CSS)
    for src, dst in ASSETS_SRC.items():
        shutil.copy(src, os.path.join(OUT, "apps", dst))
    # Seal for the homepage (also kept at the old root URL for compatibility)
    _here = os.path.dirname(os.path.abspath(__file__))
    shutil.copy(os.path.join(_here, "assets-src", "oakencode-seal.jpg"),
                os.path.join(OUT, "assets", "img", "oakencode-seal.jpg"))
    shutil.copy(os.path.join(OUT, "assets", "img", "oakencode-seal.jpg"),
                os.path.join(OUT, "oakencode-seal.jpg"))

    # Homepage (recreated from the live site, Pers-int status updated)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(page("Oakencode — Honest Software", homepage()))

    # Privacy policy (kept byte-identical to the approved page)
    os.makedirs(os.path.join(OUT, "pers-int-privacy"))
    with open(os.path.join(OUT, "pers-int-privacy", "index.html"), "w") as f:
        f.write(PRIVACY_HTML)

    # Support page
    os.makedirs(os.path.join(OUT, "support"))
    with open(os.path.join(OUT, "support", "index.html"), "w") as f:
        f.write(page("Support", support_page()))

    # Apps index
    cards = []
    for a in APPS:
        badge = f'<span class="badge {a["badge"]}">{a["status"]}</span>' if a["badge"] else f'<span class="badge">{a["status"]}</span>'
        cards.append(
            f'<a class="card" href="/apps/{a["slug"]}/">'
            f'{icon_html(a, "icon")}'
            f"<h2>{a['name']}</h2>{badge}<p>{a['tag']}</p></a>"
        )
    index_body = f"""\
<div class="hero">
  <h1>Built by a normal man, for normal people.</h1>
  <p>Every Oakencode app is offline-first, ad-free, and private by design.
  No accounts. No tracking. Your data never leaves your phone.</p>
</div>
<div class="grid">
{''.join(cards)}
</div>
<div class="teaser"><strong>On the workbench:</strong> {TEASER}</div>
{brand_strip("maestrr-founder-tie.png", ["moxie-index-a.png", "moxie-index-b.png"])}
"""
    with open(os.path.join(OUT, "apps", "index.html"), "w") as f:
        f.write(page("Apps", index_body))

    # Subpages
    for a in APPS:
        badge = f'<span class="badge {a["badge"]}">{a["status"]}</span>' if a["badge"] else f'<span class="badge">{a["status"]}</span>'
        hero = ""
        if a["hero_img"]:
            hero += f'<img class="banner" src="/apps/assets/img/{a["hero_img"]}" alt="{a["name"]} art">'
        if a["icon"]:
            hero += f'<img class="icon-lg" src="/apps/assets/img/{a["icon"]}" alt="{a["name"]} icon">'
        else:
            hero += f'<div class="icon-lg mono" style="width:120px;height:120px;border-radius:26px;font-size:3rem;margin:0 auto 1rem;">{a["mono"]}</div>'
        feats = "".join(f"<li>{x}</li>" for x in a["feats"])
        pricing = f'<section class="block"><h2>Pricing</h2><p>{a["pricing"]}</p></section>' if a["pricing"] else ""
        dlnote = f'<p class="dl-note">{a["note"]}</p>' if a.get("note") else ""
        cta = f'<div class="cta"><a class="btn" href="{a["cta"][1]}">{a["cta"][0]}</a></div>' if a["cta"] else ""
        shots = ""
        if a.get("shots"):
            figs = "".join(
                f'<figure><img src="/apps/assets/img/{img}" alt="{cap}" loading="lazy">'
                f"<figcaption>{cap}</figcaption></figure>"
                for img, cap in a["shots"]
            )
            shots = f'<section class="block"><h2>Screenshots</h2><div class="shots">{figs}</div></section>'
        body = f"""\
<div class="sub-hero">
  {hero}
  <h1>{a['name']}</h1>
  {badge}
  <p class="tagline">{a['tag']}</p>
</div>
<section class="block">
  <p>{a['desc']}</p>
</section>
<section class="block">
  <h2>Features</h2>
  <ul class="feat">{feats}</ul>
</section>
{shots}
{pricing}
{dlnote}
<div class="privacy">{PRIVACY}</div>
{cta}
<a class="back" href="/apps/">← All apps</a>
{brand_strip(a['founder'], a['strip'])}
"""
        d = os.path.join(OUT, "apps", a["slug"])
        os.makedirs(d)
        with open(os.path.join(d, "index.html"), "w") as f:
            f.write(page(a["name"], body))
    print(f"Built {len(APPS)} subpages + index into {OUT}")

if __name__ == "__main__":
    build()
