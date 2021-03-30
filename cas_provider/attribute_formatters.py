from lxml import etree
import collections

CAS_URI = 'http://www.yale.edu/tp/cas'
NSMAP = {'cas': CAS_URI}
CAS = '{%s}' % CAS_URI


try:
    basestring
except NameError:
    basestring = (str, bytes)


def jasig(auth_success, attrs):
    attributes = etree.SubElement(auth_success, CAS + 'attributes')
    style = etree.SubElement(attributes, CAS + 'attraStyle')
    style.text = 'Jasig'
    for name, value in sorted(attrs.items()):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            for e in value:
                element = etree.SubElement(attributes, CAS + name)
                element.text = e
        else:
            element = etree.SubElement(attributes, CAS + name)
            element.text = value


def ruby_cas(auth_success, attrs):
    style = etree.SubElement(auth_success, CAS + 'attraStyle')
    style.text = 'RubyCAS'
    for name, value in sorted(attrs.items()):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            for e in value:
                element = etree.SubElement(auth_success, CAS + name)
                element.text = e
        else:
            element = etree.SubElement(auth_success, CAS + name)
            element.text = value


def name_value(auth_success, attrs):
    etree.SubElement(auth_success, CAS + 'attribute', name='attraStyle', value='Name-Value')
    for name, value in sorted(attrs.items()):
        if isinstance(value, collections.Iterable) and not isinstance(value, basestring):
            for e in value:
                etree.SubElement(auth_success, CAS + 'attribute', name=name, value=e)
        else:
            etree.SubElement(auth_success, CAS + 'attribute', name=name, value=value)
