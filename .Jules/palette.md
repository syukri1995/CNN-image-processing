## 2024-05-23 - Accessibility & Responsiveness
**Learning:** Streamlit's default red (`#ff4b4b`) fails WCAG AA contrast ratio against white text (~3.9:1).
**Action:** Use `#D32F2F` (Material Red 700) for primary buttons and text to achieve ~7:1 contrast.

## 2024-05-23 - Directional Language
**Learning:** "Left panel" instructions confuse users on mobile devices where columns stack vertically.
**Action:** Use context-aware or neutral language (e.g., "Upload an image above" or "Upload an image to start").

## 2026-01-30 - Tooltips for Icon Buttons
**Learning:** Icon-only buttons (like ◀️/▶️) are inaccessible and unclear without context.
**Action:** Always add `help` tooltips to `st.button` when using icons to provide description (e.g., "Previous image").
