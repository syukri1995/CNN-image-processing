## 2024-05-23 - Accessibility & Responsiveness
**Learning:** Streamlit's default red (`#ff4b4b`) fails WCAG AA contrast ratio against white text (~3.9:1).
**Action:** Use `#D32F2F` (Material Red 700) for primary buttons and text to achieve ~7:1 contrast.

## 2024-05-23 - Directional Language
**Learning:** "Left panel" instructions confuse users on mobile devices where columns stack vertically.
**Action:** Use context-aware or neutral language (e.g., "Upload an image above" or "Upload an image to start").

## 2024-05-24 - Mobile Usability & Discovery
**Learning:** Critical model capabilities (supported classes) hidden in sidebars are missed by mobile users.
**Action:** Expose supported categories directly in the empty state (main view) to manage expectations upfront.

## 2025-02-18 - Accessibility for Icon Buttons
**Learning:** Streamlit's `st.button` does not support explicit `aria-label`.
**Action:** Always use the `help` parameter for icon-only buttons to provide a tooltip that acts as an accessible description.

## 2026-02-13 - Accessible Feedback & Dynamic Content
**Learning:** Streamlit updates content dynamically without announcing changes to screen readers by default.
**Action:** Wrap dynamic results (like predictions) in a container with `role="status"` and `aria-live="polite"` using `st.markdown` with HTML.

## 2026-02-13 - Data Consistency in UI
**Learning:** Hardcoded lists in empty states drift from actual model capabilities (e.g. casing/emojis).
**Action:** Generate empty state lists dynamically from the same `class_names` source of truth used for predictions.
