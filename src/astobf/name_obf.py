"""
all variable names are obfuscated to a string of o0Ol1I characters
"""

import ast
import random

from .constants import BUILTINS


class NameManager:
    """
    singleton class to manage variable names
    """

    def __init__(self):
        self._name_map = {}

    def get_name(self, name):
        """
        get obfuscated name for given name
        """
        if name not in self._name_map:
            while (temp := self._get_new_name()) in self._name_map.values():
                continue
            self._name_map[name] = temp
        return self._name_map[name]

    def _get_new_name(self):
        """
        get a new obfuscated name
        """
        first_char = random.choice("oOlI")
        return first_char + "".join(random.choices("o0Ol1I", k=random.randint(9, 29)))

    def get_name_map(self):
        """
        get the name map
        """
        return self._name_map


class NameObf(ast.NodeTransformer):
    """
    obfuscate all variable names
    """

    def __init__(self):
        self._name_manager = NameManager()
        self._imported_names = set()

    def visit_Import(self, node: ast.Import) -> ast.Import:  # noqa: N802
        """
        visit import node, obfuscate all imported names
        """
        for alias in node.names:
            if alias.asname is None:
                alias.asname = self._name_manager.get_name(alias.name)
            else:
                alias.asname = self._name_manager.get_name(alias.asname)
            self._imported_names.add(alias.asname)
        return node

    def visit_ImportFrom(self, node: ast.ImportFrom) -> ast.ImportFrom:  # noqa: N802
        """
        visit import from node, obfuscate all imported names
        """
        for alias in node.names:
            if alias.asname is None:
                alias.asname = self._name_manager.get_name(alias.name)
            else:
                alias.asname = self._name_manager.get_name(alias.asname)
            self._imported_names.add(alias.asname)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:  # noqa: N802
        """
        visit attribute node, obfuscate all names
        TODO: this should be an optional feature and should be disabled by default
        TODO: this should be done in a separate pass
        """
        return node
        # self.generic_visit(node)
        # if isinstance(node.value, ast.Name) and node.value.id in self._imported_names:
        #     return node
        # node.attr = self._name_manager.get_name(node.attr)
        # return node

    def visit_Name(self, node: ast.Name) -> ast.Name:  # noqa: N802
        """
        visit name node, obfuscate all names
        """
        if node.id in ("True", "False", "None") or node.id in BUILTINS:
            return node
        node.id = self._name_manager.get_name(node.id)
        return node

    def get_name_map(self):
        """
        get the name map
        """
        return self._name_manager.get_name_map()
