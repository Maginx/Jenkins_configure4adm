# -*- coding: UTF-8 -*-
from errors import *
import xml.etree.ElementTree as ET

class ConfigParser(object):
    '''Configure xml file by xml.etree.ElementTree
    '''
    def __init__(self, fpath, dest = None):
        '''Initial Configure class
        @param fpath : source file path, string
        @param dest  : dest file path, string
        '''
        self._config_xml_src = fpath
        self._config_xml_dest = dest
        if not dest:
            self._config_xml_dest = self._config_xml_src
        self.tree = ET.parse(self._config_xml_src)

    def modify_value(self, path, newValue):
        '''Modify xml file by xml property path
        @param path     : xml property full path, string
        @param newValue : modify to this value, string
        @exception XmlException
        '''
        elements = self.tree.findall(path)
        if elements.__len__() == 0:
            print 'can not find elements from path: %s' %path
            raise XmlException( 'Not found element')
        else:
            elements[0].text = newValue
            self.tree.write(self._config_xml_dest)

    def add_node(self,path,node_name,text):
        '''Add a new item to xml
        @param path      : xml parent full path, string
        @param node_name : new node name, string
        @param node_name : node inner text if exist, string
        @exception XmlException
        '''
        elements = self.tree.findall(path)
        if elements.__len__() == 0:
            print 'can not find elements from path: %s' %path
            raise XmlException( 'Not found element')
       
        for node in elements[0].getchildren():
            if node.text == text:
                return True
        node = ET.Element(node_name)
        node.text = text
        elements[0].append(node)
        self.tree.write(self._config_xml_dest)

    def add_value(self,path,text):
        ''' Append new content to exist node
        @param path : node xml path, string
        @param text : will be appended text content, string
        @exception XmlException
        @return : 0, if this content has existed in node.
        '''
        elements = self.tree.findall(path)
        if elements.__len__() == 0:
            print 'can not find elements from path: %s' %path
            raise XmlException( 'Not found element')
        if elements[0].text.find(text) >= 0:
            return 0
        elements[0].text = text + elements[0].text
        self.tree.write(self._config_xml_dest)

    def remove_node(self,path):
        '''Remove a node from xml
        @param path : node path, string
        @exception XmlException
        '''
        elements = self.tree.findall(path)
        if elements.__len__() == 0:
            print 'can not find elements from path: %s' %path
            raise XmlException( 'Not found element')
        parent_path = path.rsplit('/',1)[-2]
        parent_node = self.tree.findall(parent_path)[0]
        parent_node.remove(elements[0])
        self.tree.write(self._config_xml_dest)

    def get_node_value(self,path):
        '''Get specificed node value
        @param path : specificed node path in xml, string
        @exception XmlException
        @return : node value
        '''
        elements = self.tree.findall(path)
        if elements.__len__() == 0:
            print 'can not find elements from path: %s' %path
            raise XmlException( 'Not found element')
        return elements[0].text