from __future__ import annotations

import frappe


def get_active_apps_compat() -> list[str]:
	"""Return the active-app list across supported Frappe versions.

	Frappe 17 exposes get_active_apps(). Frappe 15/16 do not expose that API,
	so use the installed apps that are actually present on the current bench.
	"""
	get_active_apps = getattr(frappe, "get_active_apps", None)
	if callable(get_active_apps):
		return get_active_apps()
	return frappe.get_installed_apps(_ensure_on_bench=True)


def raven_installed() -> bool:
	"""True if the Raven app is available on this site and bench."""
	return "raven" in get_active_apps_compat()
