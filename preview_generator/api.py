import html as html_parser
import io

import frappe
from frappe.rate_limiter import rate_limit
from PIL import Image
from playwright.sync_api import sync_playwright


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview(html: str, format: str = "jpg") -> None:
	validate_format(format)

	with sync_playwright() as playwright:
		browser = playwright.chromium.launch()
		context = browser.new_context()
		page = context.new_page()
		page.set_content(html_parser.unescape(html))
		page.wait_for_load_state('networkidle')
		image = page.screenshot(type='jpeg', quality=30)

		if format == "webp":
			image = get_webp_image(image)

		generate_image_response(image, format)
		context.close()


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview_from_url(url: str, wait_for: int = 0, headers: dict = None, format: str = "jpg") -> None:
	validate_format(format)

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

		if format == "webp":
			image = get_webp_image(image)

		generate_image_response(image, format)
		context.close()

def generate_image_response(image_content, image_format):
	frappe.local.response.filename = f"preview.{image_format}"
	frappe.local.response.filecontent = image_content
	frappe.local.response.type = "download"


def validate_format(format: str):
	if format not in ["jpg", "webp", "jpeg"]:
		frappe.throw("Invalid format. Supported formats are jpg, jpeg and webp")

def get_webp_image(image):
	image_stream = io.BytesIO(image)
	img = Image.open(image_stream)
	output_stream = io.BytesIO()
	img.save(output_stream, format="WEBP")
	image = output_stream.getvalue()
	output_stream.close()
	image_stream.close()

	return image
