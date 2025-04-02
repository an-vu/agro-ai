# 2025

## April 2 Chanelog

### Clean up `.html` files in `app/templates/`
- `base.html`
  - Duplicate JS/CSS links, picked one version for each (Bootstrap, Font Awesome, jQuery).
  - Added charset.
  - Wrapped content in <div class="container"> for consistent layout.
  - Commented out global footer — add it back if decide to unify footers across pages.

- `index.html`
  - Removed <body> and </html>.
  - Used {{ url_for('label') }} instead of hardcoding label.html.
  - Cleaned up unnecessary <br><br><br><br><br><br> spacing.
  - Wrapped the footer in a clean, centered layout.
  - Script remains inline for now — fine since it’s short and specific.

- `label.html`
  - Removed <body> and </html>.
  - Replaced hardcoded link with {{ url_for('home') }}.
  - Used class="img-fluid" and max-width/max-height for responsive image.
  - Removed unnecessary <br> tags.
  - Cleaned script remains inline and scoped.

- `intermediate.html`
  - Removed <body>/</html>.
  - Moved the modal outside the image loops (just once on page).
  - Replaced hardcoded links with url_for(...).
  - Cleaned up spacing and popover text.
  - Combined redundant jQuery ready() calls.
  - Footer simplified and unified with other pages.

- `final.html`
  - Removed repeated modals (one shared modal at bottom).
  - Closed all <h6> tags (they were broken before).
  - Replaced hardcoded links with url_for(...).
  - Refactored JS for clarity and deduplication.

- `feedback.html`
  - Removed repeated <body>, <html>, and modal tags.
  - Fixed broken or missing </h6> tags.
  - Cleaned up redundant jQuery blocks.
  - Replaced hardcoded home redirect with url_for('index').

### Clean up `.css` files in `app/static/`

- index_format.css
  - `.start` is used, not `.image`. Remove `.image` unless it's used somewhere else.
  - fixed background-position: cover is wrong, cover is a value for background-size, not position.

- label_format.css
  - Move the image to /static/images/ and update the path

- intermediate_format.css
  - move .active_button to common.css

- final_format.css
  - Remove .active_button block
  - Consolidate modal + animation styles

- feedback_format.css

### Create `common.css`



### Add shebang to `flask_app.py`
### Might: 1. create `js` and `css` and `image` folders in `app/static/` 2. delete `styles` and move .css and image files into the folders just created.

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
