# `bandmix-cli` — Python CLI Spec for BandMix.com

## 1. Overview

A command-line tool for reading and writing data on BandMix.com. The site has no public API, so the CLI operates via authenticated HTTP requests (session cookies), scraping HTML responses and submitting standard form POSTs / AJAX calls that the site already uses. The tool targets a single logged-in user's account.

---

## 2. Authentication

The CLI authenticates via a persisted session cookie.

```
bandmix auth login --email <email>
```

Prompts interactively for the password (never accepted as a flag). On success, persists the session cookie to `~/.config/bandmix-cli/session.json`. All subsequent commands reuse this session.

```
bandmix auth logout
bandmix auth status          # prints current user screen-name and membership tier
```

Session is validated on each run; if expired, the CLI prints an error and asks the user to re-authenticate.

---

## 3. Global Flags

| Flag | Description |
|---|---|
| `--format json\|text\|table` | Output format. Default `table` for reads, `json` for piping. |
| `--raw` | Print the raw HTML response (debugging). |
| `--verbose` / `-v` | Show HTTP request details. |
| `--config <path>` | Alternate config directory. |

---

## 4. Command Reference

### 4.1 `bandmix profile`

Reads and writes the authenticated user's profile at `/account/profile/`.

#### Read

```
bandmix profile get
bandmix profile get --field description
bandmix profile get --field instruments
```

Returns all profile fields as structured data. Fields: `screen_name`, `contact_name`, `gender`, `birthdate`, `state`, `city`, `zip`, `address`, `phone`, `studio_musician`, `years_playing`, `commitment_level`, `instruments` (list), `genres` (list, max 4), `seeking_band` (bool), `seeking_instruments` (list), `description`, `influences`, `equipment`, `gigs_played`, `practice_frequency`, `gig_availability`, `most_available`.

#### Write

```
bandmix profile set --field description --value "New description text"
bandmix profile set --field genres --value "Country,Folk,Americana,Southern Rock"
bandmix profile set --field instruments --value "Vocalist,Acoustic Guitar"
bandmix profile set --field city --value "Austin"
bandmix profile set --field commitment_level --value "Very Committed"
bandmix profile set --field years_playing --value 25
```

List-valued fields accept comma-separated values. Instruments and genres are validated against the site's fixed enumerations (see §7). The CLI submits the profile form via POST to `/account/profile/`.

#### Account Type

```
bandmix profile type get              # "Musician" or "Band"
bandmix profile type set --value Band
```

Reads/writes via `/account/type/`.

---

### 4.2 `bandmix search`

Searches for musicians and bands via `/search/`. Returns paginated results.

```
bandmix search [OPTIONS]
```

| Option | Type | Description |
|---|---|---|
| `--category` | `musicians\|bands\|industry` | Profile category. Default `musicians`. |
| `--instruments` | comma-separated | Filter by instruments played. |
| `--location` | string | ZIP code or city name for search center. |
| `--radius` | `10\|25\|50\|100\|250` | Miles from location. Default 50. |
| `--sort` | `location\|activity\|date` | Sort order. |
| `--gender` | `any\|male\|female` | Gender filter. |
| `--age-from` / `--age-to` | int | Age range. |
| `--genre` | comma-separated | Filter by genre. |
| `--experience` | `beginner\|intermediate\|moderate\|advanced\|expert` | Instrument experience level. |
| `--commitment` | enum (see §7) | Commitment level. With `--commitment-mode exact\|at-least`. |
| `--keywords` | string | Free-text keyword search. |
| `--has-images` | flag | Only profiles with photos. |
| `--has-audio` | flag | Only profiles with music. |
| `--has-video` | flag | Only profiles with video. |
| `--studio` | flag | Only studio musicians. |
| `--seeking` | flag | Only those seeking musicians/bands. |
| `--active-within` | `1w\|2w\|3w\|4w\|5w\|6w` | Recency filter. |
| `--page` | int | Page number (default 1). |
| `--limit` | int | Max results to return (fetches multiple pages if needed). |

```
bandmix search --name "Jim Stone"       # Name search
bandmix search --id 123456              # ID search
```

Each result contains: `screen_name`, `slug`, `location`, `zip`, `category` (Musician/Band), `instruments`, `genres`, `seeking`, `last_active`, `has_image`, `has_audio`, `has_video`, `snippet` (description preview).

---

### 4.3 `bandmix member`

View any member's public profile by their URL slug.

```
bandmix member view <slug>
```

Returns: `screen_name`, `member_since`, `last_active`, `commitment_level`, `years_playing`, `gigs_played`, `practice_frequency`, `gig_availability`, `most_available`, `instruments` (with experience levels), `genres`, `seeking`, `description`, `influences`, `equipment`, `location`, `images` (URLs), `audio_tracks` (titles), `videos` (titles/URLs).

```
bandmix member add-to-list <slug>       # Add to Music List (bookmark)
bandmix member remove-from-list <slug>  # Remove from Music List
bandmix member hide <slug>              # Add to hidden users
bandmix member unhide <slug>            # Remove from hidden users
```

---

### 4.4 `bandmix matches`

View dashboard match results from `/account/connections/`.

```
bandmix matches list                           # New Matches (type=1), default
bandmix matches list --type new-members        # New Local Members (type=2)
bandmix matches list --page 2
```

Each result: `screen_name`, `slug`, `location`, `zip`, `instruments`, `genres`, `last_active`, `category`, `snippet`.

---

### 4.5 `bandmix messages`

Read and compose messages via `/account/messages/`. Note: sending messages requires Premier membership.

```
bandmix messages list                         # List message threads
bandmix messages read <thread_id>             # Read a conversation
bandmix messages send <slug> --body "text"    # Send a message (Premier only)
```

---

### 4.6 `bandmix feed`

Activity feed from `/account/feeds/`.

```
bandmix feed list                              # All activity
bandmix feed list --filter local               # Local activity only
bandmix feed list --filter music-list          # Music List activity only
bandmix feed list --filter my-feeds            # My own activity
bandmix feed list --limit 20
```

Each entry: `user_screen_name`, `user_slug`, `location`, `action_type` (joined, uploaded_images, uploaded_music, added_videos, updated_instruments, updated_seeking, changed_picture), `timestamp`, `detail` (contextual data).

```
bandmix feed like <feed_id>
bandmix feed unlike <feed_id>
```

---

### 4.7 `bandmix photos`

Manage photos via `/account/images/`.

```
bandmix photos list                           # List all uploaded photos (id, url, is_main)
bandmix photos upload <file_path>...          # Upload 1+ images (jpeg/png, max 24MB each)
bandmix photos set-main <photo_id>            # Set a photo as the main profile picture
bandmix photos delete <photo_id>...           # Delete photos by ID
bandmix photos reorder <id1> <id2> <id3>...   # Set display order
```

Limits: 10 photos for free accounts, 50 for Premier.

---

### 4.8 `bandmix music`

Manage audio tracks via `/account/audio/`.

```
bandmix music list                            # List tracks (id, title, type, size, has_mastered)
bandmix music upload <file_path> --title "Song Title"
bandmix music delete <track_id>...
bandmix music master <track_id>               # Submit track for BandMix mastering
bandmix music master-status <track_id>        # Check mastering progress (polls /ajax/audio-mastering-progress/)
bandmix music download-master <track_id> --format mp3|wav
```

---

### 4.9 `bandmix videos`

Manage YouTube video links via `/account/video/`.

```
bandmix videos list                           # List videos (id, title, youtube_url, visible)
bandmix videos add --title "Title" --url "https://youtube.com/watch?v=..." [--visible]
bandmix videos delete <video_id>...
bandmix videos reorder <id1> <id2> <id3>...   # Reorder via /ajax/reorder-videos/
```

---

### 4.10 `bandmix calendar`

Manage calendar events via `/account/calendar/`.

```
bandmix calendar list                          # List events (id, datetime, title, description)
bandmix calendar add --date "2026-04-14" --time "22:30" --title "Open Mic" --description "..."
bandmix calendar delete <event_id>...
```

---

### 4.11 `bandmix seeking`

Manage "Now Seeking" / wanted ads via `/account/ads/`.

```
bandmix seeking get                           # Current seeking status
bandmix seeking set --join-band true          # Set "looking to join a band"
bandmix seeking set --instruments "Lead Guitar,Bass Guitar,Drums,Banjo,Mandolin"
```

---

### 4.12 `bandmix musiclist`

Manage saved profiles (bookmarks) via `/account/bookmarks/`.

```
bandmix musiclist list                        # List bookmarked profiles
bandmix musiclist add <slug>
bandmix musiclist remove <slug>
```

---

### 4.13 `bandmix hidden`

Manage hidden/blocked users via `/account/hidden/`.

```
bandmix hidden list
bandmix hidden add <slug>
bandmix hidden remove <slug>
```

---

### 4.14 `bandmix settings`

Account settings from various options pages.

#### Email Options (`/account/email/`)

```
bandmix settings email get
bandmix settings email set --newsletters enabled|disabled
bandmix settings email set --user-views enabled|disabled
bandmix settings email set --user-visited enabled|disabled
bandmix settings email set --user-music-lists enabled|disabled
bandmix settings email set --general-notifications enabled|disabled
bandmix settings email set --format html|plaintext
```

#### Match Mailer (`/account/email/#matchmailer`)

```
bandmix settings matchmailer get
bandmix settings matchmailer set --enabled true --radius 50 --age-from 25 --age-to 55
bandmix settings matchmailer set --filter-instrument true --filter-genre true
bandmix settings matchmailer set --recommendations enabled --additional-local enabled
```

#### Dashboard Options (`/account/dashboard-options/`)

```
bandmix settings dashboard get
bandmix settings dashboard set --show-matches true --radius 100 --age-from 20 --age-to 60
```

#### Password

```
bandmix settings password update              # Prompts interactively for old + new password
```

---

## 5. Architecture

```
bandmix-cli/
├── bandmix_cli/
│   ├── __init__.py
│   ├── main.py              # Click/Typer CLI entrypoint, group definitions
│   ├── auth.py              # Login, session persistence, session validation
│   ├── client.py            # HTTP client (requests.Session wrapper, cookie jar)
│   ├── parser.py            # BeautifulSoup HTML parsers, one per page type
│   ├── models.py            # Pydantic models for all data entities
│   ├── enums.py             # Instrument, Genre, State, Commitment enums
│   ├── commands/
│   │   ├── profile.py
│   │   ├── search.py
│   │   ├── member.py
│   │   ├── matches.py
│   │   ├── messages.py
│   │   ├── feed.py
│   │   ├── photos.py
│   │   ├── music.py
│   │   ├── videos.py
│   │   ├── calendar.py
│   │   ├── seeking.py
│   │   ├── musiclist.py
│   │   ├── hidden.py
│   │   └── settings.py
│   └── formatters.py        # table/json/text output renderers
├── tests/
├── pyproject.toml
└── README.md
```

**Key dependencies:** `click` (CLI framework), `requests` (HTTP), `beautifulsoup4` + `lxml` (HTML parsing), `pydantic` (data models/validation).

---

## 6. HTTP Transport Details

The site uses standard HTML form submissions and a handful of AJAX endpoints. The CLI must:

- Maintain a `requests.Session` with cookie persistence across calls.
- Extract CSRF tokens from forms if present (hidden input fields) and include them in POSTs.
- Set a realistic `User-Agent` header.
- Follow redirects (302s after form submissions).
- For file uploads (photos, music), use `multipart/form-data` encoding. The photo uploader uses Dropzone.js on the frontend, but the backend accepts standard multipart POST to `/account/images/`.

**Known AJAX endpoints** (discovered from page JavaScript):

| Endpoint | Method | Purpose |
|---|---|---|
| `/ajax/sort-images/` | POST | Reorder photos (serialized sortable list) |
| `/ajax/rotate-image/` | POST | Rotate image (`img`, `angle` params) |
| `/ajax/reorder-videos/` | POST | Reorder video list |
| `/ajax/audio-mastering/` | POST | Initiate mastering (`audio` param) |
| `/ajax/audio-mastering-progress/` | GET | Poll mastering progress (`audio` param) → `{progress, id}` |
| `/ajax/audio-mastered/` | GET | Get mastered track info (`audio` param) → `{container, content}` |
| `/account/feeds-load/` | GET | Load activity feed (`feeds_show` param) |
| `/account/feeds-load-comments/` | POST | Load comments for feed item (`feed` param) |

---

## 7. Enumerations

**Instruments** (36 values): Accordion, Acoustic Guitar, Background Singer, Bagpipes, Banjo, Bass Guitar, Cello, Clarinet, DJ, Dobro, Drums, Electronic Music, Fiddle, Flute, Harmonica, Harp, Keyboard, Lead Guitar, Mandolin, Other, Other Percussion, Piano, Rhythm Guitar, Saxophone, Steel guitar, Trombone, Trumpet, Ukulele, Upright bass, Violin, Vocalist, Vocalist - Alto, Vocalist - Baritone, Vocalist - Bass, Vocalist - Soprano, Vocalist - Tenor.

**Genres** (max 4 selectable, 33 values): Acoustic, Alternative, Americana, Bluegrass, Blues, Calypso, Celtic, Christian / Gospel, Christian Contemporary, Classic Rock, Classical, Country, Cover/Tribute, Dubstep, Electronic, Folk, Funk, Hip Hop/Rap, Jazz, Latin, Lounge, Metal, Other, Pop, Progressive, Punk, R&B, Reggae, Rock, Ska, Southern Rock, World.

**Commitment Levels**: Just for Fun, Moderately Committed, Committed, Very Committed, Touring.

**Instrument Experience**: Beginner, Intermediate, Moderate, Advanced, Expert.

**Years Playing**: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60+.

**Gigs Played**: Unspecified, Under 10, 10 to 50, 50 to 100, Over 100.

**Practice Frequency**: Unspecified, 1 time per week, 2-3 times per week, More than 3 times per week.

**Gig Nights/Week**: Unspecified, 1 night a week, 2-3 nights a week, 4-5 nights a week, 6-7 nights a week.

**Availability**: Unspecified, Mornings, Days, Nights.

**Search Categories**: Musicians, Bands, Industry Listings (subcategories: Songwriters, Photographers, Venues, Independent labels, Management, Music stores, Recording studios, Lightings, Sound engineers, Music teachers, Rehearsal space).

**US States**: All 50 states plus DC, territories (AS, GU, MH, FM, MP, PW, PR, VI), and Armed Forces regions (Americas, Europe, Pacific).

---

## 8. Error Handling

- **Session expired**: HTTP 302 redirect to login page → `AuthenticationError`, prompt re-login.
- **Premier required**: Detected from page content (e.g., messaging blocked) → `PremierRequiredError` with descriptive message.
- **Validation errors**: Enum/value mismatches caught at the CLI layer before submission, with suggestions (e.g., "Did you mean 'Acoustic Guitar'?"). Fuzzy matching on instrument/genre names.
- **Rate limiting / server errors**: Retry with exponential backoff (3 attempts, 1s/2s/4s).
- **Form submission failures**: Parse response HTML for error messages and surface them.

---

## 9. Configuration File

Optional `~/.config/bandmix-cli/config.toml`:

```toml
[defaults]
format = "table"
search_radius = 50
search_location = "76710"

[session]
path = "~/.config/bandmix-cli/session.json"
```

---

## 10. Example Workflows

```bash
# Log in
bandmix auth login --email jim@example.com

# View your full profile
bandmix profile get

# Update description
bandmix profile set --field description --value "Updated band description..."

# Search for drummers within 50 miles playing country
bandmix search --instruments Drums --genre Country --radius 50 --active-within 2w

# View a match's full profile
bandmix member view darrell1917056

# Add them to your music list
bandmix member add-to-list darrell1917056

# Check your activity feed
bandmix feed list --limit 10

# Upload a new track
bandmix music upload ./my-song.mp3 --title "Dusty Roads"

# Add a gig to your calendar
bandmix calendar add --date 2026-05-01 --time "20:00" --title "Open Mic at Common Grounds"

# Export search results as JSON for scripting
bandmix search --instruments "Lead Guitar" --genre "Country,Folk" --format json > leads.json
```