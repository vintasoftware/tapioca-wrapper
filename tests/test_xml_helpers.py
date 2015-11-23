# coding: utf-8

import unittest
from collections import OrderedDict
from xml.etree import ElementTree
from tapioca.xml_helpers import (
    etree_elt_dict_to_xml, flat_dict_to_etree_elt_dict, xml_string_to_etree_elt_dict,
    input_branches_to_xml_bytestring)


# Use sets of 3 to test the translation methods
# Note: There are limitations to the 'flat' format when compared to ElementTree.Element, so these
# tests don't yet cover the full range of inputs to etree_elt_dict_to_xml()
FLAT_1 = {'root1|attr1="my attr value 1"|attr2="my attr value 2"': 'root text'}
ETREE_DICT_1 = {'tag': 'root1',
                       'attrib': {'attr1': 'my attr value 1',
                                  'attr2': 'my attr value 2'},
                       'text': 'root text',
                       'tail': None,
                       'sub_elts': None}
XML_STR_1 = '<root1 attr1="my attr value 1" attr2="my attr value 2">root text</root1>'

FLAT_2 = {'root2|attr1="my attr value 1"': {
          'subroot1|subattr1="sub attr value 1"': 'subtext 1'}}
ETREE_DICT_2 = {'tag': 'root2',
                'attrib': {'attr1': 'my attr value 1'},
                'text': None,
                'tail': None,
                'sub_elts': [{'tag': 'subroot1',
                              'attrib': {'subattr1': 'sub attr value 1'},
                              'text': 'subtext 1',
                              'tail': None,
                              'sub_elts': None}]
                }
XML_STR_2 = ('<root2 attr1="my attr value 1"><subroot1 subattr1="sub attr value 1">'
             'subtext 1</subroot1></root2>')

FLAT_3 = {'root2|attr1="my attr value 1"': {
          'subroot1|subattr1="sub attr value 1"': {
              'subroot2|subattr2="sub attr value 2"': 'subtext 2'}
          }}
ETREE_DICT_3 = {'tag': 'root2',
                'attrib': {'attr1': 'my attr value 1'},
                'text': None,
                'tail': None,
                'sub_elts': [{'tag': 'subroot1',
                              'attrib': {'subattr1': 'sub attr value 1'},
                              'text': None,
                              'tail': None,
                              'sub_elts': [{'tag': 'subroot2',
                                            'attrib': {'subattr2': 'sub attr value 2'},
                                            'text': 'subtext 2',
                                            'tail': None,
                                            'sub_elts': None}]
                              }]
                }
XML_STR_3 = ('<root2 attr1="my attr value 1">'
             '<subroot1 subattr1="sub attr value 1">'
             '<subroot2 subattr2="sub attr value 2">'
             'subtext 2'
             '</subroot2></subroot1></root2>')
FLAT_MULT = {'root1|attr1="my attr value 1"|attr2="my attr value 2"': 'root text',
             'root2|attr1="my attr value 1"':
                 {'subroot1|subattr1="sub attr value 1"': 'subtext 1'}
             }
ETREE_DICT_MULT = [{'tag': 'root2',
                    'attrib': {'attr1': 'my attr value 1'},
                    'text': None,
                    'tail': None,
                    'sub_elts': [{'tag': 'subroot1',
                                  'attrib': {'subattr1': 'sub attr value 1'},
                                  'text': 'subtext 1',
                                  'tail': None,
                                  'sub_elts': None}]
                    },
                   {'tag': 'root1',
                    'attrib': {'attr1': 'my attr value 1',
                               'attr2': 'my attr value 2'},
                    'text': 'root text',
                    'tail': None,
                    'sub_elts': None}]

FLAT_MULT_SUB = {'root|attr1="val 1"': OrderedDict([('subroot1|attr1="sub val 1"', 'sub text 1'),
                                                    ('subroot2|attr2="sub val 2"', 'sub text 2')])}

ETREE_DICT_MULT_SUB = {'tag': 'root',
                       'attrib': {'attr1': 'val 1'},
                       'text': None,
                       'tail': None,
                       'sub_elts': [{'tag': 'subroot1',
                                     'attrib': {'attr1': 'sub val 1'},
                                     'text': 'sub text 1',
                                     'tail': None,
                                     'sub_elts': None},
                                    {'tag': 'subroot2',
                                     'attrib': {'attr2': 'sub val 2'},
                                     'text': 'sub text 2',
                                     'tail': None,
                                     'sub_elts': None}]
                       }
XML_STR_MULT_SUB = ('<root attr1="val 1">'
                    '<subroot1 attr1="sub val 1">sub text 1</subroot1>'
                    '<subroot2 attr2="sub val 2">sub text 2</subroot2>'
                    '</root>')


class TestFlatToEtree(unittest.TestCase):

    def test_raises_exception_when_input_is_wrong(self):
        d = {'abc'}

        self.assertRaises(Exception, flat_dict_to_etree_elt_dict, d)

    def test_raises_exception_when_child_type_is_wrong(self):
        d = {'root2|attr1="my attr value 1"': [
            'subroot1|subattr1="sub attr value 1"', 'subtext 1'
            ]
        }

        self.assertRaises(Exception, flat_dict_to_etree_elt_dict, d)

    def test_one_level(self):
        d = FLAT_1
        expected_out = ETREE_DICT_1

        out = flat_dict_to_etree_elt_dict(d)

        self.assertEqual(out, expected_out)

    def test_two_levels(self):
        d = FLAT_2
        expected_out = ETREE_DICT_2

        out = flat_dict_to_etree_elt_dict(d)

        self.assertEqual(out, expected_out)

    def test_three_levels(self):
        d = FLAT_3
        expected_out = ETREE_DICT_3

        out = flat_dict_to_etree_elt_dict(d)

        self.assertEqual(out, expected_out)

    def test_multiple_root_nodes_raises_exception(self):
        d = FLAT_MULT

        self.assertRaises(Exception, etree_elt_dict_to_xml, d)

    def test_multiple_sub_nodes(self):
        d = FLAT_MULT_SUB
        expected_out = ETREE_DICT_MULT_SUB

        out = flat_dict_to_etree_elt_dict(d)

        for key in out.keys():
            if key != 'sub_elts':
                self.assertEqual(out[key], expected_out[key])
        self.assertEqual(out['sub_elts'][0], expected_out['sub_elts'][0])
        self.assertEqual(out['sub_elts'][1], expected_out['sub_elts'][1])


class TestEtreeEltDictToXML(unittest.TestCase):

    def test_raises_exception_when_input_is_wrong(self):
        d = ['abc']

        self.assertRaises(Exception, etree_elt_dict_to_xml, d)

    def test_one_level(self):
        d = ETREE_DICT_1
        expected_out = XML_STR_1.encode('utf-8')

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)

    def test_two_levels(self):
        d = ETREE_DICT_2
        expected_out = XML_STR_2.encode('utf-8')

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)

    def test_three_levels(self):
        d = ETREE_DICT_3
        expected_out = XML_STR_3.encode('utf-8')

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)

    def test_multiple_root_nodes_raises_exception(self):
        d = ETREE_DICT_MULT

        self.assertRaises(Exception, etree_elt_dict_to_xml, d)

    def test_multiple_sub_nodes(self):
        d = ETREE_DICT_MULT_SUB
        expected_out = XML_STR_MULT_SUB.encode('utf-8')

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)


class TestXMLInputBranches(unittest.TestCase):

    def test_branch_etree_element(self):
        elt = ElementTree.fromstring(XML_STR_MULT_SUB)
        expected_out = XML_STR_MULT_SUB.encode('utf-8')

        out = input_branches_to_xml_bytestring(elt)

        self.assertEqual(out, expected_out)

    def test_branch_xml_string(self):
        xml = XML_STR_MULT_SUB
        expected_out = XML_STR_MULT_SUB.encode('utf-8')

        out = input_branches_to_xml_bytestring(xml)

        self.assertEqual(out, expected_out)

    def test_branch_etree_elt_dict(self):
        d = ETREE_DICT_MULT_SUB
        expected_out = XML_STR_MULT_SUB.encode('utf-8')

        out = input_branches_to_xml_bytestring(d)

        self.assertEqual(out, expected_out)

    def test_branch_flat_dict(self):
        d = FLAT_MULT_SUB
        expected_out = XML_STR_MULT_SUB.encode('utf-8')

        out = input_branches_to_xml_bytestring(d)

        self.assertEqual(out, expected_out)

    def test_raises_exception_if_wrong_input(self):
        d = ['abc']

        self.assertRaises(Exception, input_branches_to_xml_bytestring, d)


class TestXMLStringToEtreeEltDict(unittest.TestCase):

    def test_xml_string_to_etree_elt_dict(self):
        xml = XML_STR_MULT_SUB
        expected_out = ETREE_DICT_MULT_SUB

        out = xml_string_to_etree_elt_dict(xml)

        for key in out.keys():
            if key != 'sub_elts':
                self.assertEqual(out[key], expected_out[key])
        self.assertEqual(out['sub_elts'][0], expected_out['sub_elts'][0])
        self.assertEqual(out['sub_elts'][1], expected_out['sub_elts'][1])

if __name__ == '__main__':
    unittest.main()
