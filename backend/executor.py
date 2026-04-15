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
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def get_state(self):
        """Returns the current state of the page in a way the LLM can understand."""
        if not self.page:
            return {"error": "No page active"}
        
        url = self.page.url
        content = await self.page.content()
        # Simplify content: get text and relevant interactive elements
        # We can extract buttons, inputs, and links specifically
        interactive_elements = await self.page.evaluate('''() => {
            const elements = document.querySelectorAll('button, input, a, form');
            return Array.from(elements).map(el => {
                return {
                    tag: el.tagName,
                    text: el.innerText || el.value || el.placeholder || '',
                    type: el.type || '',
                    name: el.name || '',
                    id: el.id || ''
                };
            });
        }''')
        
        return {
            "url": url,
            "elements": interactive_elements,
            "text": await self.page.inner_text('body')
        }

    async def navigate(self, url):
        await self.page.goto(url)
        await asyncio.sleep(1) # Small wait for stability

    async def click(self, text):
        """Clicks an element containing the specific text."""
        # Try finding by text
        try:
            # More robust selector for text matches
            await self.page.click(f"text='{text}'", timeout=5000)
        except:
            # Fallback for exact matches or specific button types
            try:
                await self.page.click(f"button:has-text('{text}')", timeout=5000)
            except:
                # Last ditch: try finding any element with that text
                await self.page.click(f"css=*:has-text('{text}')", timeout=5000)
        await asyncio.sleep(1)

    async def type(self, label_or_placeholder, value):
        """Types value into a field identified by its label or placeholder."""
        # Try finding by placeholder
        try:
            await self.page.fill(f"input[placeholder='{label_or_placeholder}']", value)
        except:
            try:
                # Try finding by label or name
                await self.page.fill(f"input[name='{label_or_placeholder}']", value)
            except:
                # Last ditch: try finding by previous label text
                await self.page.type(f"text='{label_or_placeholder}'", value)
        await asyncio.sleep(0.5)

    async def submit(self):
        await self.page.keyboard.press("Enter")
        await asyncio.sleep(1)
