import html as html_parser
import io

import frappe
from frappe.rate_limiter import rate_limit
from PIL import Image
from playwright.sync_api import sync_playwright


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview(html: str, format: str = "jpg") -> None:
	if format not in ["jpg", "webp", "jpeg"]:
		frappe.throw("Invalid format. Supported formats are jpg, jpeg and webp")

	with sync_playwright() as playwright:
		browser = playwright.chromium.launch()
		context = browser.new_context()
		page = context.new_page()
		page.set_content(html_parser.unescape(html))
		page.wait_for_load_state('networkidle')
		image = page.screenshot(type='jpeg', quality=30)

		if format == "webp":
			image_stream = io.BytesIO(image)
			img = Image.open(image_stream)
			output_stream = io.BytesIO()
			img.save(output_stream, format="WEBP")
			image = output_stream.getvalue()
			output_stream.close()
			image_stream.close()

		generate_image_response(image, format)
		context.close()

def generate_image_response(image_content, image_format):
	frappe.local.response.filename = f"preview.{image_format}"
	frappe.local.response.filecontent = image_content
	frappe.local.response.type = "download"
