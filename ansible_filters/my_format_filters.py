#!/usr/bin/env python
"""

Tue Apr 7 9:46:07 AM 2020

__author__ = "Jose Lima"

"""


class FilterModule:
    """ formatting and transformation filters """

    def filters(self):
        return {
            "str_to_list": self.str_to_list,
            "list_to_str": self.list_to_str,
            "file_to_ansible": self.file_to_ansible,
        }

    def str_to_list(self, my_str):
        """returns clean list from a string with out nulls"""
        return [x for x in my_str.splitlines() if x != ""]

    def list_to_str(self, my_list):
        """returns a clean string from a list joined by a new line"""
        return "\n".join(my_list)

    def file_to_ansible(self, cfg):
        """ return a dictionary that mocks same haiviour as ansible register """
        d = {}
        d.setdefault("stdout", [cfg])
        d.setdefault("stdout_lines", [cfg.splitlines()])
        return d
