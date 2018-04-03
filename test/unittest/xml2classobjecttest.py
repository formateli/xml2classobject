# This file is part of Xml2ClassObject project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

"Xml2ClassObject test"


from xml2classobject import Xml2ClassObject
import unittest


class Xml2ClassObjectTest(unittest.TestCase):
    def test_xml2classobject(self):
        string_xml = """
            <pjjobs>
                <Element1>Element1 text</Element1>
                <Element2>Element2 text</Element2>
                <Element3 attr1="val1" attr2="val2">Element3 text</Element3>
                <Element4>
                    <Element41>Element41 text</Element41>
                    <Element42 attr1="val142" attr2="val242">Element42 text</Element42>
                </Element4>
                <Elements>
                    <El>A</El>
                    <El>B</El>
                    <El>
                        <ElementX>Element X</ElementX>
                    </El>
                </Elements>
                <Element5 attr1="val15" attr2="val25"/>
            </pjjobs>"""

        obj = Xml2ClassObject(string_xml)

        self.assertEqual(obj.Element1.value, 'Element1 text')
        self.assertEqual(obj.Element1._section_name, 'Element1')
        self.assertEqual(obj.Element2.value, 'Element2 text')
        self.assertEqual(obj.Element2._section_name, 'Element2')
        self.assertEqual(obj.Element3.value, 'Element3 text')
        self.assertEqual(obj.Element3.attr1, 'val1')
        self.assertEqual(obj.Element3.attr2, 'val2')
        self.assertEqual(obj.Element4.Element41.value, 'Element41 text')
        self.assertEqual(obj.Element4.Element42.value, 'Element42 text')
        self.assertEqual(obj.Element4.Element42.attr1, 'val142')
        self.assertEqual(obj.Element4.Element42.attr2, 'val242')

        eles = obj.Elements.get_childs('El')
        self.assertEqual(eles[0].value, 'A')
        self.assertEqual(eles[0]._section_name, 'El')
        self.assertEqual(eles[1].value, 'B')
        self.assertEqual(eles[2].value, None)
        self.assertEqual(eles[2].ElementX.value, 'Element X')

        self.assertEqual(obj.Element4.get_childs('Element41')[0].value, 'Element41 text')
        self.assertEqual(obj.Element4.get_childs('Element41')[0]._section_name, 'Element41')

        self.assertEqual(obj.Element5.value, None)
        self.assertEqual(obj.Element5.attr1, 'val15')
        self.assertEqual(obj.Element5.attr2, 'val25')
