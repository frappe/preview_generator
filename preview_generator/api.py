from playwright.sync_api import sync_playwright

@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview(html):
	with sync_playwright() as p:

		browser = p.chromium.launch()
		page = browser.new_page()
		page.set_content(html)
		page.wait_for_load_state('networkidle')
		# page.screenshot(path=output_path, quality=30, type='jpeg')
		image = page.screenshot(type='jpeg', quality=30)
		frappe.local.response.filename = 'preview.jpg'
		frappe.local.response.filecontent = image
		browser.close()
