# coding: utf-8

import unittest

from tapioca.xml_helpers import flat_dict_to_etree_elt_dict
from tapioca.xml_helpers import etree_elt_dict_to_xml


# Use sets of 3 to test the translation methods
# Note: There are limitations to the 'flat' format when compared to ElementTree.Element, so these
# tests don't yet cover the full range of inputs to etree_elt_dict_to_xml()
FLAT_1 = {'root1|attr1="my attr value 1"|attr2="my attr value 2"': 'root text'}
ETREE_DICT_1 = {'tag': 'root1',
                       'attrib': {'attr1': 'my attr value 1',
                                  'attr2': 'my attr value 2'},
                       'text': 'root text',
                       'tail': '',
                       'sub_elts': ''}
XML_STR_1 = b'<root1 attr1="my attr value 1" attr2="my attr value 2">root text</root1>'

FLAT_2 = {'root2|attr1="my attr value 1"': {
          'subroot1|subattr1="sub attr value 1"': 'subtext 1'}}
ETREE_DICT_2 = {'tag': 'root2',
                'attrib': {'attr1': 'my attr value 1'},
                'text': '',
                'tail': '',
                'sub_elts': [{'tag': 'subroot1',
                              'attrib': {'subattr1': 'sub attr value 1'},
                              'text': 'subtext 1',
                              'tail': '',
                              'sub_elts': ''}]
                }
XML_STR_2 = (b'<root2 attr1="my attr value 1"><subroot1 subattr1="sub attr value 1">'
             b'subtext 1</subroot1></root2>')

FLAT_3 = {'root2|attr1="my attr value 1"': {
          'subroot1|subattr1="sub attr value 1"': {
              'subroot2|subattr2="sub attr value 2"': 'subtext 2'}
          }}
ETREE_DICT_3 = {'tag': 'root2',
                'attrib': {'attr1': 'my attr value 1'},
                'text': '',
                'tail': '',
                'sub_elts': [{'tag': 'subroot1',
                              'attrib': {'subattr1': 'sub attr value 1'},
                              'text': '',
                              'tail': '',
                              'sub_elts': [{'tag': 'subroot2',
                                            'attrib': {'subattr2': 'sub attr value 2'},
                                            'text': 'subtext 2',
                                            'tail': '',
                                            'sub_elts': ''}]
                              }]
                }
XML_STR_3 = (b'<root2 attr1="my attr value 1">'
             b'<subroot1 subattr1="sub attr value 1">'
             b'<subroot2 subattr2="sub attr value 2">'
             b'subtext 2'
             b'</subroot2></subroot1></root2>')
FLAT_MULT = {'root1|attr1="my attr value 1"|attr2="my attr value 2"': 'root text',
             'root2|attr1="my attr value 1"':
                 {'subroot1|subattr1="sub attr value 1"': 'subtext 1'}
             }
ETREE_DICT_MULT = [{'tag': 'root2',
                    'attrib': {'attr1': 'my attr value 1'},
                    'text': '',
                    'tail': '',
                    'sub_elts': [{'tag': 'subroot1',
                                  'attrib': {'subattr1': 'sub attr value 1'},
                                  'text': 'subtext 1',
                                  'tail': '',
                                  'sub_elts': ''}]
                    },
                   {'tag': 'root1',
                    'attrib': {'attr1': 'my attr value 1',
                               'attr2': 'my attr value 2'},
                    'text': 'root text',
                    'tail': '',
                    'sub_elts': ''}]

FLAT_MULT_SUB = {'root|attr1="val 1"': {'subroot1|attr1="sub val 1"': 'sub text 1',
                                        'subroot2|attr2="sub val 2"': 'sub text 2'}}

ETREE_DICT_MULT_SUB = {'tag': 'root',
                       'attrib': {'attr1': 'val 1'},
                       'text': '',
                       'tail': '',
                       'sub_elts': [{'tag': 'subroot1',
                                     'attrib': {'attr1': 'sub val 1'},
                                     'text': 'sub text 1',
                                     'tail': '',
                                     'sub_elts': ''},
                                    {'tag': 'subroot2',
                                     'attrib': {'attr2': 'sub val 2'},
                                     'text': 'sub text 2',
                                     'tail': '',
                                     'sub_elts': ''}]
                       }
XML_STR_MULT_SUB = (b'<root attr1="val 1">'
                    b'<subroot1 attr1="sub val 1">sub text 1</subroot1>'
                    b'<subroot2 attr2="sub val 2">sub text 2</subroot2>'
                    b'</root>')


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
        for d in out['sub_elts']:
            self.assertIn(d, expected_out['sub_elts'])


class TestEtreeEltDictToXml(unittest.TestCase):

    def test_raises_exception_when_input_is_wrong(self):
        d = ['abc']

        self.assertRaises(Exception, etree_elt_dict_to_xml, d)

    def test_one_level(self):
        d = ETREE_DICT_1
        expected_out = XML_STR_1

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)

    def test_two_levels(self):
        d = ETREE_DICT_2
        expected_out = XML_STR_2

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)

    def test_three_levels(self):
        d = ETREE_DICT_3
        expected_out = XML_STR_3

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)

    def test_multiple_root_nodes_raises_exception(self):
        d = ETREE_DICT_MULT

        self.assertRaises(Exception, etree_elt_dict_to_xml, d)

    def test_multiple_sub_nodes(self):
        d = ETREE_DICT_MULT_SUB
        expected_out = XML_STR_MULT_SUB

        out = etree_elt_dict_to_xml(d)

        self.assertEqual(out, expected_out)  # potential sequencing issue


class TestEtreeNodeToEltDict(unittest.TestCase):

    def test_etree_node_to_etree_elt_dict(self):
        pass


if __name__ == '__main__':
    unittest.main()
