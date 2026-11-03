# Final Project Plan

## Sketch

The design sketch is kept in a separate file while it is being finalized: [`sketch/sketch.svg`](./sketch/sketch.svg) (PNG copy: [`sketch/sketch.png`](./sketch/sketch.png)).

It shows the signed-out and signed-in screens with their URLs, the shared navigation bar, and the UI elements for each CRUD operation.

## Narrative

### ShotCoach

**Team:** Team ShotCoach
**Student:** Alex Grant

#### Purpose

ShotCoach helps photographers improve by learning directly from professional work. A user uploads a photo they took, or types out an idea for a shot, and ShotCoach finds professional reference photos that match its concept and style. It then explains, in plain language, what the user could change to get closer to that result.

Most people learn photography by guessing. They take a photo, feel it's "not quite right," and don't know why. Finding examples means scrolling through Pinterest or Instagram with no explanation of how a photo was made. Classes and mentors help, but they cost money and aren't available when you're out shooting.

ShotCoach closes that gap. It pairs a photo with relevant pro examples and turns the differences into specific, actionable tips about lighting, composition, angle, and camera settings. That makes feedback fast, free, and tied to the user's own work.

#### Users

The primary users are beginner and intermediate photographers, especially students and hobbyists who shoot on a phone or an entry-level camera. They are motivated to get better but don't have a mentor, can't afford workshops, and often don't know the vocabulary to search for what they want ("low-key lighting," "shallow depth of field").

A second group is photographers planning a shoot. They already have an idea in mind and want references to show a model or friend, plus a place to keep them organized.

ShotCoach benefits these users in three ways:

- **No vocabulary required.** Users describe an idea in their own words, or just upload a photo, and the app generates the search terms for them.
- **Feedback that fits them.** Tips account for the user's gear and skill level from their profile, so a phone shooter isn't told to buy a new lens.
- **Progress over time.** Every coached shot is saved, so users can look back and see how their work has changed.

#### Features

- **Photo upload + AI coaching:** A user uploads a photo. A vision-capable LLM describes its subject, lighting, and style and generates search keywords. ShotCoach pulls matching photos from the Pexels API, re-ranks them by visual similarity with a CLIP image model, and has the LLM write improvement tips comparing the user's photo to the top matches.
- **Idea search:** A user types an idea and the app shows reference photos plus the AI-generated keywords.
- **Settings comparison:** The app reads the photo's EXIF data (aperture, shutter speed, ISO, focal length) and shows it next to typical settings from the pro references. GPS data is stripped before the photo is stored.
- **Boards:** Users save references to boards for planned shoots, with an optional shoot date and location.
- **Profile:** Gear and skill level personalize the coaching.

**Example:** Alex uploads a night portrait from his phone. ShotCoach suggests the keywords "night portrait, neon light, low key," shows eight similar pro shots, and notes that the pros shoot lower, use a wider aperture, and use a faster shutter. Alex saves two references to his "Downtown neon shoot" board for next week.

#### Data

Users create, read, update, and delete **Shots** (their uploaded photos and coaching) and **Boards** (saved references for a shoot). They read and update their **Profile**. **References** and **Critiques** are created by the app and read by users.

| Model | Properties (type) |
| --- | --- |
| **Profile** | user (OneToOne → User), skill_level (choice: beginner/intermediate/advanced), camera (string), lenses (string), favorite_styles (string) |
| **Shot** | owner (FK → User), image (image file), title (string), idea_text (text, optional), keywords (JSON list), aperture (decimal), shutter_speed (string), iso (integer), focal_length (integer), created_at (datetime) |
| **Critique** | shot (FK → Shot), tips (text), model_name (string), created_at (datetime) |
| **Reference** | pexels_id (integer, unique), image_url (URL), page_url (URL), photographer (string), alt_text (string) |
| **ShotMatch** | shot (FK → Shot), reference (FK → Reference), similarity (float 0–1), rank (integer) |
| **Board** | owner (FK → User), name (string), description (text), shoot_date (date, optional), location (string, optional), references (ManyToMany → Reference) |

**Relationships:** A User has one Profile, many Shots, and many Boards. A Shot has many Critiques. Shots and References are many-to-many through ShotMatch, which stores the similarity score. Boards and References are many-to-many.

**Sample data:**

```
Shot:      { title: "Neon portrait", idea_text: "Moody portrait under neon signs",
             keywords: ["night portrait", "neon light", "low key"],
             aperture: 2.8, shutter_speed: "1/60", iso: 800, focal_length: 26 }
Critique:  { tips: "Shoot from lower so the signs frame you. Open to f/1.8...",
             model_name: "gemini-flash" }
ShotMatch: { reference: Pexels #3812345 by "A. Rivera", similarity: 0.94, rank: 1 }
Board:     { name: "Downtown neon shoot", shoot_date: 2026-11-21, location: "Main St.",
             references: [3812345, 2901774] }
```

## Claims

Solo project goal: an **A**, meaning all Basic claims, 8 Intermediate claims, and 1 Stretch claim, plus extras for bonus points. See [claims.md](./claims.md).

### Basic (all)

| Claim | How ShotCoach meets it |
| --- | --- |
| B10 Front page | Landing page with idea search and how-it-works steps (`/`) |
| B20 Navigation | Shared nav bar in the base template on every page |
| B30 Django admin | All models registered in `/admin/` |
| B40 3 distinct models | Profile, Shot, Critique, Reference, ShotMatch, Board |
| B50 Database persistence | All data stored with the Django ORM |
| B60 404 handling | Custom 404 page in the site's style |
| B70 Relationships | ForeignKeys, OneToOne (Profile), ManyToMany (Boards, ShotMatch) |
| B80 URL routing | Readable URLs such as `/shots/42/edit/` and `/boards/7/` |
| B90 Templates | All pages rendered with Django templates |
| B100 Template inheritance | `base.html` extended by every page |
| B110 Consistent styling | One black-and-white stylesheet across all pages |
| B120 Styled forms | Labeled, styled upload, shot, board, and profile forms |
| B121 Automated a11y | Pages pass WAVE checks (alt text, labels, contrast) |
| B130–B160 CRUD | Full CRUD for Shots and Boards |
| B170 Login/logout | Django authentication |
| B180 Enforced authentication | Shots, Boards, and Profile require login |
| B190 Security | `{% csrf_token %}` on all forms, CSRF middleware enabled |

### Intermediate (8)

| Claim | How ShotCoach meets it |
| --- | --- |
| I10 File uploads | Users upload their photos to create Shots |
| I20 Search | Idea search through Pexels, plus search/filter over the user's own shots and boards |
| I30 User profiles | Editable profile with gear and skill level, used in the coaching prompt |
| I40 Pagination | Search results, My Shots, and coaching history |
| I50 Input validation | Upload type/size checks, required titles, no shoot dates in the past |
| I70 External API | Pexels API for reference photos |
| I90 Mobile-responsive | Layout works at 375px so users can upload from their phones |
| I180 Logging | Logs LLM/API calls, latency, and failures |

**Backups / extra +10s:** I150 bulk remove on boards, I60 export a board as a shot list (CSV/JSON), I130 charts of progress or settings over time, I100 in-app camera basics help page.

### Stretch

| Claim | How ShotCoach meets it |
| --- | --- |
| **S110 LLM integration** (A claim) | Vision LLM analyzes photos, generates search keywords, and writes coaching tips |
| **S100 ML integration** (+50 second Stretch) | CLIP image embeddings re-rank references by visual similarity |
