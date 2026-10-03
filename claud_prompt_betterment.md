# Prompt: David Sudher Ministries Website Update

## Role

You are a senior Django developer and web designer. Update the existing Django project (`David_Anna`, app `ministry`) as described below. Read `PROJECT_ARCHITECTURE.md` first. Make the changes directly in the codebase, keep the current visual style, and do not add new dependencies unless stated.

---

## 1. Goals

1. Remove the **Blog** section and replace it with a **Testimonies** section that uses the same layout format as the blog.
2. Remove the **Ministry** page and move its content into the **Home** page.
3. Remove the **Invite David to Speak** feature everywhere.
4. Move the images from the Ministry page into the **About** page.
5. Fix the design problems and add the SEO items listed below.

---

## 2. Navigation (final)

**Home · About · Messages · Testimonies · Events · Contact**

- Style **Contact** as the gold button (the only call-to-action in the nav).
- Remove the old gold "Invite David to Speak" button.
- Remove the floating "Invite David" button at the bottom right of every page.
- Remove Blog, Ministry and Invite links from the nav and footer.
- Footer columns: ministry blurb, **Explore** (Home, About, Messages, Testimonies), **Connect** (Today's Word, Events, Media, Contact).
- Hide the "Connect with David" social block unless real links exist in the admin. No placeholder text may show on the public site.

---

## 3. Remove "Invite David to Speak"

- Delete `invite.html`, its view and its URL.
- Add a **301 redirect** from `/invite/` to `/contact/`.
- Remove every "Invite David" button and link in all templates (home, footer, "Join David" section, base layout).
- Where a button is still needed, use "Contact" or "Get in touch".
- In the contact form, keep the "Speaking Invitations" topic.

---

## 4. Replace Blog with Testimonies

### Model

Create a `Testimony` model (or repurpose the article model with a migration that preserves data safely):

| Field | Type | Notes |
|---|---|---|
| `name` | CharField | Person's name |
| `location` | CharField | City / country, optional |
| `title` | CharField | Short headline |
| `slug` | SlugField | Unique, auto-generated from title |
| `story` | TextField | Full testimony |
| `excerpt` | CharField | Optional. Auto-generate from story if empty |
| `photo` | ImageField | Optional, upload to `media/testimonies/` |
| `video_url` | URLField | Optional YouTube link |
| `category` | CharField (choices) | Salvation, Healing, Provision, Family, Calling, Deliverance |
| `is_featured` | BooleanField | Default False |
| `is_published` | BooleanField | **Default False** |
| `consent_given` | BooleanField | Required on submission |
| `created_at` | DateTimeField | auto_now_add |

Register it in `admin.py` with list filters (category, published, featured), search (name, title, story) and an action "Publish selected".

### Pages

- `/testimonies/`: list page
  - Hero: label "TESTIMONIES", heading "Stories of what God has done", one short line below.
  - Category filter pills (All, Salvation, Healing, Provision, Family, Calling, Deliverance), using the same style as the old blog filters.
  - One featured testimony at the top (large, with photo and pull quote).
  - 2-column card grid below: photo or initials circle, 2-line excerpt, name and location, "Read story" link.
  - Only show `is_published=True`.
- `/testimonies/<slug>/`: detail page
  - Narrow reading column (about 680px), large opening quote, the story, optional video, then "Share your own story".
- **Share your story form** (on the list page, in a calm cream panel):
  - Fields: name, city, title, story, optional photo, **consent checkbox** (required).
  - Submissions are saved as **unpublished** and appear only after admin approval.
  - Add spam protection (honeypot field plus simple rate limit by IP/session).
  - Validate photo type (jpg, png, webp) and size (max 5 MB).
  - Show a friendly success message after submitting.

### Cleanup

- Remove the blog views, URLs, templates (`blog.html`, `article_detail.html`) and nav/footer links.
- Add **301 redirects**: `/blog/` to `/testimonies/`, and `/blog/<slug>/` to `/testimonies/`.
- The existing blog articles are teachings, not testimonies. Do not convert them automatically. List them in the final summary so the owner can decide what to do with them.
- Update `seed_content.py` with 3 to 4 sample testimonies (marked as sample content).

---

## 5. Remove the Ministry page, merge into Home

- Delete `ministry.html`, its view and URL.
- Add a **301 redirect** from `/ministry/` to `/#vision`.
- Home page order:
  1. **Hero**: full-width photo with dark overlay, one headline, one sentence, two buttons ("Watch Messages", "Read David's Story").
  2. **Vision** (`id="vision"`): dark section, "Raise. Equip. Send.", three cards.
  3. **What we do**: 2 to 3 alternating image/text rows using the short Ministry copy (for example "Grow. Then go."). Keep text short with a "Read more" link to About.
  4. **A message without borders**: India, Pakistan, United States, with a clean SVG map and three gold pins (replace the current brown blobs).
  5. **Latest messages**: 3 video cards with real thumbnails.
  6. **Testimonies preview**: one featured quote in large serif type and a "Read more stories" link.
  7. **Upcoming events**: keep the existing list.
  8. **Scripture banner**, then **newsletter**.
- Do not repeat the same copy in two places on the home page.

---

## 6. Move Ministry images to About

- Reuse the images from the old Ministry page (already in `static/ministry/images/`). Do not duplicate the files.
- Replace **every** "[Add image here later]" box on `about.html`.
- Suggested placement:
  - Before "A Growing Hunger for God": the prayer photo.
  - Before "The Journey Continues": a ministry or discipleship photo.
  - After the closing prayer: a portrait of David.
- Use at most 3 images, alternating full-width and half-width.
- Add a descriptive `alt` text to each image and a short italic caption in the same style as "Leader. Mentor. Minister. Witness."
- If any placeholder has no image, remove the empty box.
- Style the closing prayer as a centered pull quote with a thin gold rule above it.
- Use bold only for the single most important sentence in each section.

---

## 7. Design requirements

Keep the current look: charcoal-black, warm cream, muted gold, with the serif heading font and the sans body font already in use.

- **Colors:** gold is for primary buttons, small labels and thin dividers only.
- **Text:** body text at least 17px with line-height 1.7. Small gold uppercase labels at 12 to 13px, in a darker gold on cream backgrounds so contrast passes WCAG AA.
- **Spacing:** one consistent section rhythm, about 96px top/bottom on desktop and 56px on mobile.
- **Buttons:** two styles only: solid gold (primary) and outlined (secondary). Change the black "View all messages" style buttons to outlined.
- **Header:** slightly translucent with a subtle blur on scroll.
- **Newsletter block:** show on Home and in the footer only, not on every page.
- **Messages page:**
  - Fix the broken YouTube embeds. Use a thumbnail with a play icon, and load the player only on click using `youtube-nocookie.com`.
  - Replace "Message One / Message Two" with real titles, a date and a one-line description.
  - Show the latest message as a larger featured card at the top.
  - If a video cannot be embedded, show a "Watch on YouTube" link instead of an error box.
- **Mobile:** hamburger menu with a full-screen overlay, single-column card grids, full-width buttons, readable hero text over photos.
- **Images:** use fewer, better photos. Do not repeat the same photo across cards.

---

## 8. SEO requirements

- Unique `<title>` (under 60 characters) and meta description (under 160 characters) on every page, set through template blocks in `base.html`.
- Exactly one `<h1>` per page, using descriptive text (for example "Contact David Sudher Ministries").
- Canonical URL tag on every page.
- Open Graph and Twitter Card tags (title, description, image, URL) with a default image fallback.
- `sitemap.xml` using `django.contrib.sitemaps` (static pages, events, messages, published testimonies) and a `robots.txt` that links to it.
- JSON-LD structured data:
  - `Organization` / `Person` on About
  - `Event` on event detail pages
  - `VideoObject` on messages
- Images: WebP where possible, `width` and `height` attributes, `loading="lazy"` below the fold, and meaningful `alt` text.
- Use real place names in content (Bangalore, Hyderabad, India, Pakistan, United States).
- Make sure no page ships with placeholder text.

---

## 9. Rules

- Do not break existing pages: Home, About, Messages, Events, Contact, Today's Word, Media, Privacy, Terms.
- Run and create migrations cleanly. Do not delete `db.sqlite3`.
- Keep `settings.py` secure for production (`DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`) and mention anything that needs changing before deployment.
- Write or update tests in `ministry/tests.py` for: the testimony submission (unpublished by default), the list page showing only published entries, and the redirects.
- Do not invent testimonies, names or quotes for real people. Use clearly marked sample content only.

---

## 10. Acceptance checklist

- [ ] Nav shows exactly: Home, About, Messages, Testimonies, Events, Contact
- [ ] No "Invite David" text or button anywhere (nav, footer, floating, home, forms)
- [ ] `/invite/`, `/blog/`, `/blog/<slug>/` and `/ministry/` redirect with 301 to the right pages
- [ ] Testimonies list and detail pages work, with category filters and the featured entry
- [ ] Submitted testimonies stay unpublished until approved in the admin
- [ ] Home page contains the Ministry content with no duplicated copy
- [ ] About page has the Ministry images, with alt text and captions, and no placeholder boxes
- [ ] Messages page has no broken embeds and has real titles
- [ ] Every page has a unique title, meta description, one H1, canonical and Open Graph tags
- [ ] `sitemap.xml` and `robots.txt` work
- [ ] Site looks right on mobile
- [ ] Tests pass and migrations apply cleanly

---

## 11. Deliverable

When finished, give a short summary that lists:

1. Files created, changed and deleted.
2. Migrations to run.
3. Anything that needs the owner's input (real video links, social links, old blog articles, final images).