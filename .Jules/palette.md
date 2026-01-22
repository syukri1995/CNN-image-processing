## 2026-01-22 - Improved Empty State Guidance
**Learning:** Users arriving at the main screen see a file uploader but may not immediately know *what* to upload or what the model supports. A generic "Upload here" message is functional but cold.
**Action:** Replace empty states with "What to expect" content. Listing supported categories (Burger, Sushi, etc.) in the empty state sets clear expectations and acts as a mini-onboarding step. This is more effective than hiding this info in the sidebar.

## 2026-01-22 - ARIA Live Regions for Dynamic Content
**Learning:** Streamlit updates content dynamically (like prediction results) without a page reload. Screen readers often miss these updates.
**Action:** Always wrap dynamic result containers in an element with `role="alert"` or `aria-live="polite"`. This forces the screen reader to announce the new content immediately. Added this to the `prediction-box`.
