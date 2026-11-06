import os
from playwright.sync_api import sync_playwright

def capture():
    os.makedirs('screenshots', exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        url = 'file:///' + os.path.abspath('web-dashboard/redesign.html').replace('\\', '/')
        
        # 1. Desktop Dark
        page = browser.new_page(viewport={'width': 1440, 'height': 900})
        page.add_init_script("localStorage.setItem('bluestar_device_pin', '1234'); localStorage.setItem('bluestar_theme', 'dark');")
        page.goto(url)
        page.wait_for_timeout(3000)
        page.screenshot(path='screenshots/redesign_desktop_dark.png')
        
        # Scroll right column to view features and convertible mode
        page.evaluate("document.querySelector('.control-console').scrollTop = 500")
        page.wait_for_timeout(600)
        page.screenshot(path='screenshots/redesign_desktop_dark_scrolled.png')

        # 2. Desktop Light
        page.evaluate("toggleTheme()")
        page.evaluate("document.querySelector('.control-console').scrollTop = 0")
        page.wait_for_timeout(800)
        page.screenshot(path='screenshots/redesign_desktop_light.png')
        page.evaluate("document.querySelector('.control-console').scrollTop = 500")
        page.wait_for_timeout(600)
        page.screenshot(path='screenshots/redesign_desktop_light_scrolled.png')

        # 3. Mobile Dark
        page_mobile = browser.new_page(viewport={'width': 390, 'height': 844})
        page_mobile.add_init_script("localStorage.setItem('bluestar_device_pin', '1234'); localStorage.setItem('bluestar_theme', 'dark');")
        page_mobile.goto(url)
        page_mobile.wait_for_timeout(3000)
        page_mobile.screenshot(path='screenshots/redesign_mobile_dark.png')
        page_mobile.evaluate("window.scrollTo(0, 360)")
        page_mobile.wait_for_timeout(600)
        page_mobile.screenshot(path='screenshots/redesign_mobile_dark_scrolled.png')

        # 4. Mobile Light
        page_mobile.evaluate("toggleTheme()")
        page_mobile.evaluate("window.scrollTo(0, 0)")
        page_mobile.wait_for_timeout(800)
        page_mobile.screenshot(path='screenshots/redesign_mobile_light.png')

        browser.close()
    print("Full captures complete!")

if __name__ == '__main__':
    capture()
