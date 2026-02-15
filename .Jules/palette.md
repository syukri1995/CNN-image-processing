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

## 2025-02-27 - Streamlit Accessibility Patterns
**Learning:** Streamlit's `st.info` and `st.success` are not automatically announced by screen readers when dynamically updated. Injecting semantic HTML via `st.markdown` with `role="status"` and `aria-live="polite"` is crucial for accessible status updates (like prediction results).
**Action:** Always wrap dynamic result containers in semantic HTML with live region attributes when building Streamlit apps.

## 2025-02-27 - Testing UI without Heavy Models
**Learning:** Adding a `MockModel` class guarded by an environment variable allows verifying complex UI states (like prediction results) in CI/headless environments without loading large model files.
**Action:** Implement mock backends for UI verification tests to improve test reliability and speed.
