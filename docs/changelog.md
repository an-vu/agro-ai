# 2025

## April 17 Changelog
- Update index.html and finalize redesign
- Update label.html and finalize redesign

---

## April 9 Changelog

- Refactor and organize remaining pages (2nd and 3rd training phases).
- Finalize `main.js` and break into modules if needed.
- Optimize and comment `common.css` for long-term use.
- Decide how to handle image hover, selection, and feedback UX.
- Fix result page

### Finalized Frontend cleanup

- All Javascript codes are moved to `main.js` in `/app/static/js/`
- 

### Redesign Frontend
- Redesign whole looks.
- Redesign index.html
- Redesign label.html


### What's Next


---

## April 2 Changelog

### HTML Cleanup (`app/templates/`)

- **`base.html`**
  - Removed duplicate CSS/JS links (Bootstrap, Font Awesome, jQuery).
  - Added charset meta tag.
  - Wrapped `{% block content %}` in `<div class="container">` for layout consistency.
  - Commented out footer block — re-enable if unifying footers later.

- **`index.html`**
  - Removed `<body>` and `</html>` tags.
  - Replaced hardcoded `label.html` with `{{ url_for('label') }}`.
  - Removed excessive `<br>` tags.
  - Improved layout using `.card`, `.column-container`, and `.row-container`.
  - Applied new button style (`.button.primary-button`).
  - Hero section reworded and styled for modern look.
  - Background image issue fixed with proper `bg-image` class.

- **`label.html`**
  - Removed `<body>` and `</html>`.
  - Replaced hardcoded link with `{{ url_for('home') }}`.
  - Image now uses `.img-fluid` with responsive constraints.
  - Cleaned up spacing and `<br>` tags.
  - Kept scoped inline script — minimal and specific.

- **`intermediate.html`**
  - Removed duplicate modals inside loops — now placed once at bottom.
  - Used `url_for(...)` instead of hardcoded links.
  - Unified tooltip/popover logic.
  - Cleaned layout and JS structure.

- **`final.html`**
  - Reused single shared modal at bottom.
  - Fixed all unclosed `<h6>` tags.
  - Replaced all hardcoded links with `url_for(...)`.
  - Refactored JS for better structure and DRY logic.

- **`feedback.html`**
  - Removed redundant `<body>`/`<html>` tags and modal duplication.
  - Fixed broken closing tags.
  - Consolidated jQuery logic.
  - Used `url_for('home')` instead of hardcoded redirect.

### CSS Cleanup (`app/static/styles/`)

- **Removed:** `index_format.css`, `intermediate_format.css`, `feedback_format.css`
  - All duplicate `.active_button` styles and modals consolidated.
  - Fixed incorrect `background-position: cover` (was invalid CSS).

- **`label_format.css`**
  - Moved `bgimageblur.jpg` to `static/images/`, updated path accordingly.

- **`final_format.css`**
  - Removed `.active_button` styles.
  - Consolidated modal, zoom animation, and close button styles into shared CSS.

- **New:** `common.css`
  - Global button styles (`.button`, `.primary-button`, `.secondary-button`, etc.)
  - Global modal styles
  - Card layout (`.card`, `.row-container`, `.column-container`)
  - Background animation and typography
  - Title text styles (`.main-title`, `.sub-title`, `.card-label`)

### JavaScript

- **New:** `main.js`
  - Moved all page-specific jQuery DOM logic into one organized file.
  - Each view’s behavior is gated using `body.dataset.page` for scope.
  - Reduced duplication and made logic more maintainable.

### Other

- Added shebang (`#!/usr/bin/env python3`) to `flask_app.py`
- Moved `bgimageblur.jpg` to `app/static/images/`

---

## March 12 Changelog

### `app/` Updates
- Added `archive/` folder to store unused codes.
- Moved `ImagePreprocessing.py` inside `archive/`.

---

## March 5 Changelog

### `docs/` Updates
- Moved the `dox/` folder and `index.html` into the `2020/` folder.
- Renamed `dox/` and `index.html` with a `2020_` prefix to prevent conflicts with newer files.
- Added a new `Doxygen` folder for the latest 2025 documentation.
- Created a `png/` folder to store images:
  - `backend.png`: Backend code documentation.
  - `directory-tree.png`: Directory tree visualization.
- Added `docs_overview.md` for documentation structure.
- Added `changelog.md` to track changes.

---
