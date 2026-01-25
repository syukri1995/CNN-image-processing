## 2025-10-26 - Streamlit Responsive Instructions
**Learning:** Using directional language like "left panel" in Streamlit columns is problematic because columns stack vertically on mobile devices, making the instruction confusing.
**Action:** Use device-agnostic language like "Upload an image" or conditional logic if checking for mobile (though hard in Streamlit) is not possible.

## 2025-10-26 - Brand Color Contrast
**Learning:** The default brand color `#ff4b4b` often used in Streamlit themes fails WCAG AA on white backgrounds (~3.3:1).
**Action:** Use `#D32F2F` (Material Red 700) or darker for text and primary buttons to ensure accessibility while maintaining the brand hue.
