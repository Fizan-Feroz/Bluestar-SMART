import os
from playwright.sync_api import sync_playwright

def capture():
    os.makedirs('screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        # Desktop Redesign
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        url = 'file:///' + os.path.abspath('web-dashboard/redesign.html').replace('\\', '/')
        page.add_init_script("localStorage.setItem('bluestar_device_pin', '1234'); localStorage.setItem('bluestar_theme', 'dark');")
        page.goto(url)
        page.wait_for_timeout(3500)
        page.screenshot(path='screenshots/redesign_desktop_dark.png')
        page.evaluate("toggleTheme()")
        page.wait_for_timeout(1000)
        page.screenshot(path='screenshots/redesign_desktop_light.png')
        
        # Mobile Redesign
        page_mobile = browser.new_page(viewport={'width': 390, 'height': 844})
        page_mobile.add_init_script("localStorage.setItem('bluestar_device_pin', '1234'); localStorage.setItem('bluestar_theme', 'dark');")
        page_mobile.goto(url)
        page_mobile.wait_for_timeout(3000)
        page_mobile.screenshot(path='screenshots/redesign_mobile_dark.png')
        page_mobile.evaluate("toggleTheme()")
        page_mobile.wait_for_timeout(1000)
        page_mobile.screenshot(path='screenshots/redesign_mobile_light.png')
        
        browser.close()
    print("Captures complete!")

if __name__ == '__main__':
    capture()
