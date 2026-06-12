import html as html_parser

import frappe
from frappe.rate_limiter import rate_limit
from frappe.utils.preview import get_preview_from_html, get_preview_from_url


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview(html: str, format: str = "jpg") -> None:
	# html arrives escaped over the wire; the framework renders it and validates format.
	set_response(get_preview_from_html(html_parser.unescape(html), format=format), format)


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=60, seconds=60)
def generate_preview_from_url(url: str, wait_for: int = 0, headers: dict = None, format: str = "jpg") -> None:
	set_response(get_preview_from_url(url, wait_for=wait_for, headers=headers, format=format), format)


def set_response(image: bytes, format: str) -> None:
	frappe.local.response.filename = f"preview.{format}"
	frappe.local.response.filecontent = image
	frappe.local.response.type = "download"
