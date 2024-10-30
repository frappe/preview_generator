import frappe
from playwright.sync_api import sync_playwright
from frappe.rate_limiter import rate_limit
import html as html_parser

@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview(html):
	with sync_playwright() as playwright:
		browser = playwright.chromium.launch()
		context = browser.new_context()
		page = context.new_page()
		page.set_content(html_parser.unescape(html))
		page.wait_for_load_state('networkidle')
		image = page.screenshot(type='jpeg', quality=30)
		frappe.local.response.filename = 'preview.jpg'
		frappe.local.response.filecontent = image
		frappe.local.response.type = "download"
		context.close()


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview_from_url(url: str, wait_for: int = 0, headers: dict = None):
	with sync_playwright() as playwright:
		browser = playwright.chromium.launch()
		context = browser.new_context(
			extra_http_headers=headers or {}
		)
		page = context.new_page()
		page.goto(url)
		page.wait_for_load_state('networkidle')
		if wait_for:
			page.wait_for_timeout(wait_for)
		image = page.screenshot(type='jpeg', quality=30)
		frappe.local.response.filename = 'preview.jpg'
		frappe.local.response.filecontent = image
		frappe.local.response.type = "download"
		context.close()
