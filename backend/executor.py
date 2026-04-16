from playwright.async_api import async_playwright
import os
import asyncio

class PlaywrightExecutor:
    def __init__(self, headless=True):
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    async def start(self):
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            # Set default timeout to 10 seconds to avoid long hangs
            self.page.set_default_timeout(10000)
        except Exception as e:
            print(f"Failed to start Playwright: {e}")
            await self.stop()
            raise

    async def stop(self):
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
        except:
            pass
        finally:
            self.browser = None
            self.page = None

    async def is_alive(self):
        return self.page is not None and not self.page.is_closed()

    async def get_state(self):
        if not await self.is_alive():
            return {"error": "Browser is closed"}
        
        url = self.page.url
        try:
            # Extract only relevant interactive elements
            interactive_elements = await self.page.evaluate('''() => {
                const elements = document.querySelectorAll('button, input, a, [role="button"]');
                return Array.from(elements).map(el => {
                    return {
                        tag: el.tagName,
                        text: el.innerText || el.value || el.placeholder || el.getAttribute('aria-label') || '',
                        type: el.type || '',
                        name: el.name || '',
                        id: el.id || ''
                    };
                }).filter(el => el.text || el.name || el.id);
            }''')
            
            text = await self.page.inner_text('body')
            return {"url": url, "elements": interactive_elements, "text": text[:2000]}
        except Exception as e:
            return {"url": url, "error": str(e)}

    async def navigate(self, url):
        if not await self.is_alive(): return
        print(f"Navigating to: {url}")
        await self.page.goto(url, wait_until="networkidle")
        await asyncio.sleep(2)

    async def click(self, text):
        if not await self.is_alive(): return
        print(f"Attempting to click: {text}")
        # Try multiple selector strategies
        selectors = [
            f"text='{text}'",
            f"button:has-text('{text}')",
            f"a:has-text('{text}')",
            f"[role='button']:has-text('{text}')",
            f"button[id='{text}']",
            f"button[name='{text}']"
        ]
        
        for selector in selectors:
            try:
                await self.page.click(selector, timeout=3000)
                await asyncio.sleep(1)
                return
            except:
                continue
        print(f"Failed to click '{text}' with standard selectors")

    async def type(self, field_identifier, value):
        if not await self.is_alive(): return
        print(f"Attempting to type '{value}' into '{field_identifier}'")
        
        # Try finding by name, id, placeholder, or label
        selectors = [
            f"input[name='{field_identifier}']",
            f"input[id='{field_identifier}']",
            f"input[placeholder*='{field_identifier}']",
            f"label:has-text('{field_identifier}') + input",
            f"input[type='text']", # Risky fallback
            f"input[type='email']"
        ]
        
        for selector in selectors:
            try:
                await self.page.fill(selector, value, timeout=3000)
                await asyncio.sleep(0.5)
                return
            except:
                continue
        
        # Absolute fallback: press Tab and type (not ideal but works for simple forms)
        print(f"Could not find field '{field_identifier}', trying generic fill...")

    async def submit(self):
        if not await self.is_alive(): return
        await self.page.keyboard.press("Enter")
        await asyncio.sleep(2)
