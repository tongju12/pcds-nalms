#! /usr/bin/env python
from __future__ import print_function
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring
from xml.dom import minidom
import yaml
import types
import sys
import collections
 
 
directory = './'
alarm_server = 'nalms-kfe'
yamlfile = '/Users/fmurgia/Documents/SLAC/pcds-nalms/Spreadsheet/RTDSK0Vac.yaml'
xmlfile = '/Users/fmurgia/Documents/SLAC/pcds-nalms/XML/RTDSK0Vac.xml'
 
def yaml2xml(obj, level, rootElement):
    pvs = []
 
    if isinstance(obj, dict):
        if 'pv' in obj:
            sub = SubElement(rootElement, 'pv')
            sub.set('name',obj['pv'])
            if(obj['pv'] in pvs):
                print('duplicate pv: ', obj['pv'], ' in file: ', yamlfile)
                sys.exit(1)
            pvs.append(obj['pv'])
            for name, value in obj.items():
                if name == 'pv':
                    continue
                att = SubElement(sub, name)
                if not isinstance(value, (dict, list)):
                    att.text = xstr(value)
                else:
                    yaml2xml(value, level+1, att)
 
        elif 'pvs' in obj:
            yaml2xml(obj['pvs'], level, rootElement)
            if 'automated_action' in obj:
                sub = SubElement(rootElement,'automated_action')
                yaml2xml(obj['automated_action'], level+1, sub)
        else:
            for k in obj.keys():
                if k in ('details', 'title', 'delay'):
                    sub = SubElement(rootElement,k)
                    sub.text = xstr(obj[k])
                else:
                    sub = SubElement(rootElement,'component')
                    sub.set('name',k)
                yaml2xml(obj[k],level+1,sub)
    elif isinstance(obj, list):
        for item in obj:
            yaml2xml(item, level+1, rootElement)
 
''' From https://stackoverflow.com/questions/5121931
 
    Remap yaml loader to use an OrderedDict, preserving top-level components.
    Should not be necessary in python 3.6 (or just > 3.x).
'''
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
 
def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())
 
def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))

def xstr(s):
    if s is None:
        return ''
    return str(s)
 
yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)
 
def main():
    try:
        with open(yamlfile,'r') as f:
            contents = f.read()
        obj = yaml.safe_load(contents)
        root = Element('config')
        root.set('name', alarm_server)
        level = 1
        yaml2xml(obj, level, root)
        xmlstr = minidom.parseString(tostring(root, encoding='utf8', method='xml'))
        xmlstr = xmlstr.toprettyxml(indent="   ")
        with open(xmlfile, "wb") as f:
          f.write(xmlstr.encode('utf-8'))
        sys.exit(0)
    except (Exception) as e:
        raise
 
if __name__ == '__main__':
    main()
