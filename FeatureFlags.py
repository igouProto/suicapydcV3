"""
Feature flags!
This all started since I need a workaround for playing YT vids with lavalink via URLs :P
"""

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)


class FeatureFlags:

	# Hardcoded flags
	DEFAULTS = {"yt_url_workaround": False}

	def __init__(self, config_path: str = "Assets/feature_flags.json"):
		self.config_path = Path(config_path)
		self.flags = {}
		self._load()

	def _load(self):
		"""
		Load flag states persisted in file
		"""
		self.flags = self.DEFAULTS.copy()

		if self.config_path.exists():
			try:
				with open(self.config_path, "r") as f:
					persisted_flag_states = json.load(f)
					self.flags.update(persisted_flag_states)
			except Exception as e:
				log.warning(f"Failed to load feature flags: {e}")

		self._save()
		
		log.info("Feature flags loaded: {}".format(self.flags))

	def _save(self):
		with open(self.config_path, "w") as file:
			json.dump(self.flags, file, indent=2)

	def enable(self, flag: str) -> bool:
		"""
		Enables a flag. Returns whether a flag exists
		"""
		if flag not in self.DEFAULTS:
			return False

		self.flags[flag] = True

		# persist
		self._save()

		return True

	def disable(self, flag: str) -> bool:
		"""
		Disables a flag. Returns whether a flag exists
		"""
		if flag not in self.DEFAULTS:
			return False

		self.flags[flag] = False

		# persist
		self._save()

		return True

	def toggle(self, flag: str) -> bool | None:
		"""
		Disables a flag. Returns the flag's new state
		(or None if flag does not exist)
		"""
		if flag not in self.DEFAULTS:
			return None

		self.flags[flag] = not self.flags[flag]

		# persist
		self._save()

		return self.flags[flag]

	def list_all(self) -> dict[str, bool]:
		return self.flags.copy()
	
	def is_enabled(self, flag: str) -> bool:
		return self.flags[flag] if self.flags[flag] else False
