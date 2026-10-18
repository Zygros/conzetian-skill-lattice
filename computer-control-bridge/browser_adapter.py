"""Playwright browser adapter for CUCB. Requires explicit install and user-owned profile."""
from __future__ import annotations
import os, time, uuid
from urllib.parse import urlparse

class BrowserAdapter:
    """Controls one visible Playwright browser context; does not export cookies."""
    def __init__(self, allowed_origins, user_data_dir, headless=False):
        if not allowed_origins:
            raise ValueError("at least one allowed origin is required")
        self.allowed_origins = set(allowed_origins)
        self.user_data_dir = user_data_dir
        self.headless = headless
        self.playwright = None
        self.context = None
        self.page = None
        self._observation_id = None
    def _check_origin(self, url):
        parsed = urlparse(url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        if parsed.scheme != "https" and not (parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}):
            raise PermissionError("only HTTPS or localhost test URLs are permitted")
        if origin not in self.allowed_origins:
            raise PermissionError("browser origin is not allowlisted")
    def _ensure_started(self):
        if self.page is not None:
            return
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError("Install optional dependency with: pip install playwright && playwright install chromium") from exc
        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir, headless=self.headless)
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.set_default_timeout(5000)
    def describe(self):
        return {"platform": "browser", "adapter": "PlaywrightBrowserAdapter",
                "adapter_status": "ready" if self.page else "not_started",
                "capabilities": ["computer.observe", "computer.click", "computer.type",
                    "computer.scroll", "browser.navigate", "browser.read_text", "browser.screenshot"],
                "real_device_access": bool(self.page), "allowed_origins": sorted(self.allowed_origins)}
    def observe(self, target):
        self._ensure_started()
        if self.page.url and self.page.url != "about:blank":
            self._check_origin(self.page.url)
        self._observation_id = "browser-obs-" + str(uuid.uuid4())
        try:
            text = self.page.locator("body").inner_text(timeout=2000)[:12000]
        except Exception:
            text = ""
        return {"target": target, "observation_id": self._observation_id,
                "timestamp": time.time(), "url": self.page.url,
                "title": self.page.title(), "visible_text": text}
    def act(self, action, args):
        self._ensure_started()
        if action == "navigate":
            self._check_origin(args["url"])
            self.page.goto(args["url"], wait_until="domcontentloaded")
        elif action == "click":
            selector = args.get("selector") or args.get("element_id")
            if not isinstance(selector, str) or not selector or len(selector) > 512:
                raise ValueError("click requires a bounded CSS selector or element id")
            if "selector" not in args:
                selector = "#" + selector
            self.page.locator(selector).first.click()
        elif action == "type_text":
            selector = args.get("selector")
            if not selector:
                raise ValueError("type_text requires an explicit selector")
            self.page.locator(selector).fill(args["text"][:4000])
        elif action == "scroll":
            amount = max(1, min(1200, int(args.get("amount", 300))))
            direction = args.get("direction", "down")
            if direction not in {"up", "down"}:
                raise ValueError("browser adapter supports vertical scrolling only")
            self.page.evaluate("(amount) => window.scrollBy(0, amount)", amount if direction == "down" else -amount)
        elif action == "read_text":
            selector = args.get("selector", "body")
            return {"visible_text": self.page.locator(selector).inner_text()[:12000], "url": self.page.url}
        elif action == "screenshot":
            path = args.get("path")
            if not isinstance(path, str) or not path or ".." in path:
                raise ValueError("screenshot requires an explicit safe output path")
            self.page.screenshot(path=path, full_page=False)
            return {"screenshot_path": path, "url": self.page.url}
        elif action == "wait":
            selector = args.get("selector")
            if not selector:
                raise ValueError("wait requires a visible CSS selector")
            self.page.locator(selector).wait_for(state="visible", timeout=min(10000, int(args.get("timeout_ms", 5000))))
        else:
            raise NotImplementedError(f"browser adapter does not implement {action}")
        return {"url": self.page.url, "title": self.page.title()}
    def close(self):
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
        self.context = self.page = self.playwright = None
