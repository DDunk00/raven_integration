from unittest import TestCase
from unittest.mock import patch

import frappe

from raven_integration.utils import get_active_apps_compat, raven_installed


class TestActiveAppsCompatibility(TestCase):
	def test_uses_native_active_apps_when_available(self):
		with patch.object(frappe, "get_active_apps", return_value=["frappe", "raven"], create=True) as active:
			with patch.object(frappe, "get_installed_apps") as installed:
				self.assertEqual(get_active_apps_compat(), ["frappe", "raven"])
				active.assert_called_once_with()
				installed.assert_not_called()

	def test_falls_back_to_installed_apps_present_on_bench(self):
		with patch.object(frappe, "get_active_apps", None, create=True):
			with patch.object(
				frappe,
				"get_installed_apps",
				return_value=["frappe", "raven"],
			) as installed:
				self.assertEqual(get_active_apps_compat(), ["frappe", "raven"])
				installed.assert_called_once_with(_ensure_on_bench=True)

	def test_raven_installed_uses_compatibility_lookup(self):
		with patch(
			"raven_integration.utils.get_active_apps_compat",
			return_value=["frappe", "raven"],
		):
			self.assertTrue(raven_installed())
