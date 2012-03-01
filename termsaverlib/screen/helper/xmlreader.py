###############################################################################
#
# file:     xmlreader.py
#
# Purpose:  refer to module documentation for details
#
# Note:     This file is part of Termsaver application, and should not be used
#           or executed separately.
#
###############################################################################
#
# Copyright 2012 Termsaver
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
###############################################################################
"""
A helper class used for screens that require XML handling. See
additional information in the class itself.

The helper class available here is:

    * `XMLReaderHelperBase`

"""

#
# Python built-in modules
#
import os
from xml.dom.minidom import parse, Node, parseString

#
# Internal modules
#
from termsaverlib.screen.helper import ScreenHelperBase
from termsaverlib import exception


class XMLReaderHelperBase(ScreenHelperBase):
    """
    This helper class will handle basic XML parsing, not trying to solve all
    mysteries of the universe here. What we are looking for are main nodes that
    contain repetitive data, commonly found on a dataset, or RSS feed. More
    complex handling is not treated at this point, but it might be implemented
    if the need surfaces.

    The basic instantiation of this class require you to inform 2 arguments:

        * `base_node`: Defines the primary node where the data must be
           retrieved from.

        * `tags`: Defines which tags within the XML must be parsed to build a
           list of dictionaries.

    Those two arguments will give the hint about where is the data and which
    piece of it you are looking for.

    For actually getting the data, you will need to:

        * prepare a raw data (file content, Internet data, etc) into a
          XML object, named `__doc`; and
        * parse the XML object into a more convenient list of dictionaries
          that will be populated in `data` property.

    To prepare the data, you have 2 options:

        * `doc_xml_string`: a method that will create a dom xml document from
          a text string (obviously it must be a XML)

        * `doc_xml_file`: a method that will create a dom xml document from
          a file content (obviously it must be a XML)

    Once you have the XML properly prepared, and stored in `__doc`, you can
    call the parsing method:

        * `parse_data`: this will actually execute the action to extract the
           information you are looking for based on the arguments passed
           in the instantiation.

    """

    __doc = None
    """
    Holds the xml.dom.minidom document object
    """

    clean_dirt = []
    """
    Holds a list of strings that will be cleaned up from each result in the
    XML data, when placing them into the `data` property. This can be pretty
    handy to remove trailing spaces, new lines, or unwanted HTML tags from the
    data.
    """

    base_node = None
    """
    Defines the primary node where the data must be retrieved from.
    """

    tags = []
    """
    Defines which tags within the XML must be parsed to build a
    list of dictionaries.
    """

    data = None
    """
    Holds a list, created from properly parsing the dom document object in
    `__doc`, as specified with `base_node` and `tags` filtering.
    """

    def __init__(self, base_node, tags):
        """
        Creates a new instance of this class.

        Arguments:

        * `base_node`: Defines the primary node where the data must be
           retrieved from.

        * `tags`: Defines which tags within the XML must be parsed to build a
           list of dictionaries.
        """
        self.base_node = base_node
        self.tags = tags

    def parse_data(self):
        """
        Only call this once you have already created the dom document object,
        by calling either `doc_xml_file` or `doc_xml_string` methods.

        This will parse the document into a list, much simpler to deal with.
        On the logic here is done, the list is available in the property `data`
        """
        def get_note_value(node, node_type):
            result = ''
            for node2 in node:
                for node3 in node2.childNodes:
                    if node3.nodeType == node_type:
                        result += node3.data
            # clean possible dirt
            for t in self.clean_dirt:
                # execute a loop here for dealing with multiple occurrences
                # (such as multiple spaces)
                while result.find(t) > -1:
                    result = result.replace(t, "")
            return result

        if self.__doc is None:
            raise Exception("""You must parse the raw data, by calling a \
doc_xml_* method to populate the dom document object.""")

        result = []
        for node in self.__doc.getElementsByTagName(self.base_node):
            temp = {}
            for tag in self.tags:
                temp[tag] = get_note_value(node.getElementsByTagName(tag),
                                           Node.TEXT_NODE)
                if not temp[tag]:
                    temp[tag] = get_note_value(node.getElementsByTagName(tag),
                                               Node.CDATA_SECTION_NODE)
            result.append(temp)
        self.data = result

    def doc_xml_file(self, path):
        """
        Parses a specified file into a xml.dom.minidom document object, to be
        used by `parse_data` method later on. This method here will store the
        result in the private `__doc` property.

        Arguments:

            * path: the XML file path that will be parsed into a dom
              document object.
        """
        if not os.path.exists(path):
            raise exception.PathNotFoundException(path)

        try:
            self.__doc = parse(path)
        except:
            raise exception.XmlException(path)

    def doc_xml_string(self, text):
        """
        Parses a specified string into a xml.dom.minidom document object, to be
        used by `parse_data` method later on. This method here will store the
        result in the private `__doc` property.

        Arguments:

            * text: the XML string value that will be parsed into a dom
              document object.
        """
        try:
            self.__doc = parseString(text)
        except:
            raise exception.XmlException(text)
