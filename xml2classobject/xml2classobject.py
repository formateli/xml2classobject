# This file is part of Xml2ClassObject project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import os
from xml.dom import minidom
from xml.parsers import expat


class _Section(object):
    def __init__(self, name, parent):
        self.value = None
        self._children = {}
        self._children_list = []
        self._section_name = name

        self._parent = parent

        if self._parent:
            self._parent.add_child(self)

    def add_child(self, child):
        if child._section_name not in self._children:
            self._children[child._section_name] = []
        self._children[child._section_name].append(child)
        self._children_list.append(child)

        children = self._children[child._section_name]
        if len(children) == 1:
            setattr(self, child._section_name, child)
        elif len(children) == 2:
            setattr(self, child._section_name, children)

    def get_childs(self, name=None):
        if name is None:
            return self._children_list
        if name in self._children:
            return self._children[name]

    def add_attr(self, name, value):
        setattr(self, name, value)

    def __getattr__(self, name):
        raise Exception("'{1}' has no attribute '{0}'".format(
            name, self._section_name))


class Xml2ClassObject(_Section):
    def __init__(self, xml):
        if xml is None:
            raise ValueError("Xml2ClassObject: Parameter 'xml' must be set.")

        try:
            if os.path.isfile(xml):
                doc = minidom.parse(xml)
            else:
                doc = minidom.parseString(xml)
        except:
            raise ValueError(
                "Xml2ClassObject: Invalid 'xml' parameter: {0}".format(
                    xml))

        node = doc.documentElement
        super(Xml2ClassObject, self).__init__(node.nodeName, None)
        self._resolve(self, node)

    @staticmethod
    def has_section(section, name):
        try:
            has = hasattr(section, name)
            return has
        except:
            return

    def _resolve(self, parent, xml_node):
        for n in xml_node.childNodes:
            if n.nodeName in ('#text', '#comment'):
                continue
            if len(n.childNodes) == 0 and not n.hasAttributes():
                continue

            section = _Section(n.nodeName, parent)
            if n.hasAttributes():
                i = 0
                while i < n.attributes.length:
                    attr = n.attributes.item(i)
                    section.add_attr(attr.name, attr.value)
                    i += 1

            if len(n.childNodes) == 1 and n.childNodes[0].nodeName == '#text':
                setattr(section, 'value', self._get_xml_tag_value(n))
            else:
                self._resolve(section, n)

    @staticmethod
    def _get_xml_tag_value(node):
        'Returns the valid value of xml node'
        xml_str = node.toxml()
        start = xml_str.find('>')
        if start == -1:
            return
        end = xml_str.rfind('<')
        if end < start:
            return
        res = Xml2ClassObject._unescape(xml_str[start + 1:end])
        return res

    @staticmethod
    def _unescape(s):
        if not isinstance(s, str):
            s = s.encode("utf-8")

        list = []

        # create and initialize a parser object
        p = expat.ParserCreate("utf-8")
        p.buffer_text = True
        p.CharacterDataHandler = list.append

        # parse the data wrapped in a dummy element
        # (needed so the "document" is well-formed)
        p.Parse("<e>", 0)
        p.Parse(s, 0)
        p.Parse("</e>", 1)

        # join the extracted strings and return
        es = ""
        return es.join(list)
