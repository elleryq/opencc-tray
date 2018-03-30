# -*- coding: utf-8 -*-
"""Config."""
import os
import json
import logging


# Compat between Python 3.4 and Python 3.5
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

logger = logging.getLogger(__name__)


class Config:
    class __Config(dict):
        def __init__(self, json_config_file=None, *args, **kwargs):
            """Constructor."""
            super().__init__(*args, **kwargs)
            if not json_config_file:
                json_config_file = os.path.join(
                    os.path.expanduser("~/.config/"),
                    "vscode-launcher-tray.json")
            self.json_config_file = json_config_file
            self.load()

        def save(self):
            """Save."""
            json.dump(self, open(self.json_config_file, "wt"))

        def load(self):
            try:
                self.update(json.load(open(self.json_config_file)))
            except (FileNotFoundError, json.JSONDecodeError) as ex:
                logger.warning("{} not found.".format(self.json_config_file))

        def get_projects(self):
            if 'projects' not in self:
                self['projects'] = []
            return self['projects']

    instance = None

    def __init__(self, json_config_file=None):
        if not Config.instance:
            Config.instance = Config.__Config(json_config_file)
        # else:
        #    Config.instance.json_config_file = json_config_file

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __contains__(self, item):
        return self.instance.__contains__(item)

    def __getitem__(self, key):
        return self.instance.__getitem__(key)

    def __setitem__(self, key, value):
        return self.instance.__setitem__(key, value)