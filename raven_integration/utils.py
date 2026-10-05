from __future__ import annotations

import frappe


def _site_apps() -> list[str]:
	"""Return active apps when Frappe supports app disabling, else installed apps.

	Older Frappe releases expose only frappe.get_installed_apps(). Newer releases
	add frappe.apps.get_active_apps(). Keep compatibility with both generations
	without changing semantics on runtimes that support disabled apps.
	"""
	try:
		from frappe.apps import get_active_apps
	except ImportError:
		return frappe.get_installed_apps()

	return get_active_apps()


def raven_installed() -> bool:
	"""True if Raven is available for this site.

	On Frappe releases that support disabling apps this means active, not merely
	installed. Older supported releases have no disabled-app state, so installed
	apps are the authoritative equivalent.
	"""
	return "raven" in _site_apps()
