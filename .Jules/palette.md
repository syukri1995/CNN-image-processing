## 2025-01-23 - Accessible Prediction Results
**Learning:** For AI prediction results, wrapping the output in a container with `role="status"` and `aria-live="polite"` is crucial for ensuring screen readers announce the result immediately upon generation, without requiring the user to navigate to find it.
**Action:** Always wrap async result containers with live region attributes.
