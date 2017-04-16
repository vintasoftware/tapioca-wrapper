from xml.etree import ElementTree
from collections import Mapping
from operator import methodcaller


def flat_dict_to_etree_elt_dict(dict_to_convert, _depth=0):
    '''
    Convert a special flat format to a dictionary that can be readily mapped to etree.Element.

    The special flat format is intended to be similar to XML arguments and easy to type while
    reading XML related API documents.

    This format does not allow for combinations of text, subelements, and tails. It supports
    either text or subelements. If you need more flexibility, use the more general etree_elt_dict
    format with the etree_elt_dict_to_xml() method.

    A single root node is required.
    Double quotes in attribute values are stripped and optional.

    Example Input:
    {'root|attr1="val 1"': {'subroot1|attr1="sub val 1"': 'sub text 1',
                            'subroot2|attr2="sub val 2"': 'sub text 2'}}
    '''
    if not _depth and len(dict_to_convert) > 1:
        raise Exception('Multiple root nodes detected, please check input has only one root node.')
    node_list = []
    for k, v in dict_to_convert.items():
        etree_elt_dict = {}
        etree_elt_dict['tag'], attrib_list = [k.split('|')[0], k.split('|')[1:]]
        etree_elt_dict['attrib'] = {k: v.replace('"', '') for k, v
                                    in map(methodcaller('split', '='), attrib_list)}

        # no support for text and subelements for any single node.
        if isinstance(v, Mapping):
            etree_elt_dict['text'] = None
            etree_elt_dict['sub_elts'] = flat_dict_to_etree_elt_dict(dict_to_convert=v,
                                                                     _depth=_depth + 1)
        elif isinstance(v, str):
            etree_elt_dict['text'] = v
            etree_elt_dict['sub_elts'] = None
        else:
            raise Exception('Child element not of type Mapping or String')

        etree_elt_dict['tail'] = None
        node_list.append(etree_elt_dict)
    if not node_list:
        node_list = None
    return node_list if _depth else node_list[0]


def _etree_elt_list_to_xml(etree_elt_list):
    '''
    Helper method to handle lists of etree_elt_dicts.
    '''
    return_list = []
    # todo: test for required keys
    for etree_elt_dict in etree_elt_list:
        if not isinstance(etree_elt_dict, Mapping):
            raise Exception('Structure must be a Mapping object')
        node = ElementTree.Element(etree_elt_dict['tag'],
                                   attrib=etree_elt_dict['attrib'])
        node.text = etree_elt_dict['text']
        node.tail = etree_elt_dict['tail']
        if etree_elt_dict['sub_elts']:
            node.extend(_etree_elt_list_to_xml(etree_elt_dict['sub_elts']))
        return_list.append(node)
    return return_list


def etree_elt_dict_to_xml(etree_elt_dict):
    '''
    Converts an etree_elt_dict into XML. There must be a single root node.
    An etree_elt_dict is designed to readily map onto ElementTree.Element.
    '''
    if not isinstance(etree_elt_dict, Mapping):
        raise Exception('Structure must be a Mapping object')
    return ElementTree.tostring(_etree_elt_list_to_xml([etree_elt_dict])[0], encoding='utf-8')


def _etree_node_to_etree_elt_dict(etree_node):
    # for output
    etree_elt_dict = {}
    etree_elt_dict['tag'] = etree_node.tag
    etree_elt_dict['attrib'] = etree_node.attrib
    etree_elt_dict['text'] = etree_node.text
    etree_elt_dict['tail'] = etree_node.tail

    sub_elts = [_etree_node_to_etree_elt_dict(n) for n in etree_node]
    if sub_elts:
        etree_elt_dict['sub_elts'] = sub_elts
    else:
        etree_elt_dict['sub_elts'] = None
    return etree_elt_dict


def xml_string_to_etree_elt_dict(xml_string):
    # for output
    return _etree_node_to_etree_elt_dict(ElementTree.fromstring(xml_string))


def input_branches_to_xml_bytestring(data):
    if type(data) == ElementTree.Element:
        return ElementTree.tostring(data, encoding='utf-8')
    elif type(data) == str:
        return data.encode('utf-8')
    elif type(data) == bytes:
        return data
    elif type(data) == dict:
        if 'tag' in data.keys():
            return etree_elt_dict_to_xml(data)
        else:
            return etree_elt_dict_to_xml(flat_dict_to_etree_elt_dict(data))
    else:
        raise Exception('Format not recognized')
