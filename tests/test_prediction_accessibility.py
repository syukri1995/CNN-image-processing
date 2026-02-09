import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright, expect

def test_prediction_accessibility():
    print("Starting Streamlit app...")

    # Environment variables
    env = os.environ.copy()
    env["MOCK_MODEL"] = "1"
    env["HEADLESS"] = "true"

    # Start process
    process = subprocess.Popen(
        ["streamlit", "run", "app.py", "--server.port=8503", "--server.headless=true"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        # Wait for server
        print("Waiting for server to start on port 8503...")
        time.sleep(10) # Give it a head start

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                page.goto("http://localhost:8503", timeout=30000)
            except Exception as e:
                print(f"Failed to load page: {e}")
                # Try to read output
                process.terminate()
                stdout, stderr = process.communicate()
                print("STDOUT:", stdout)
                print("STDERR:", stderr)
                sys.exit(1)

            print("Page loaded. Uploading image...")

            # Locate file input
            # Streamlit usually hides the input but we can target it
            file_input = page.locator("input[type=file]")

            # Prepare image path
            image_path = os.path.abspath("dataset/train/pizza/001.jpg")

            if not os.path.exists(image_path):
                print(f"Image not found at {image_path}")
                sys.exit(1)

            # Upload
            file_input.set_input_files(image_path)

            print("Image uploaded. Waiting for prediction...")

            # Wait for prediction box
            # It has class 'prediction-box'
            prediction_box = page.locator(".prediction-box")

            # Use expect to wait
            expect(prediction_box).to_be_visible(timeout=30000)

            print("Prediction visible. Checking attributes...")

            role = prediction_box.get_attribute("role")
            aria_live = prediction_box.get_attribute("aria-live")

            print(f"Found role: {role}")
            print(f"Found aria-live: {aria_live}")

            if role != "status":
                print("FAIL: role is not 'status'")
                sys.exit(1)

            if aria_live != "polite":
                print("FAIL: aria-live is not 'polite'")
                sys.exit(1)

            print("SUCCESS: Accessibility attributes present!")

            # Take screenshot
            os.makedirs("verification", exist_ok=True)
            screenshot_path = os.path.abspath("verification/accessibility_fix.png")
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Try to read output if process is still running
        if process.poll() is None:
             process.terminate()
             stdout, stderr = process.communicate()
             print("STDOUT:", stdout)
             print("STDERR:", stderr)
        sys.exit(1)

    finally:
        if process.poll() is None:
            print("Terminating process...")
            process.terminate()
            process.wait()

if __name__ == "__main__":
    test_prediction_accessibility()
