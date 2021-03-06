#===============================================================================
#
#  Flatmap viewer and annotation tools
#
#  Copyright (c) 2019  David Brooks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#===============================================================================

from datetime import datetime, timezone

#===============================================================================

from lxml import etree

#===============================================================================

from mapmaker import __version__

from .. import EXCLUDE_SHAPE_TYPES, EXCLUDE_TILE_LAYERS
from ..markup import parse_markup
from .utils import adobe_decode

#===============================================================================

class SVGCleaner(object):
    def __init__(self, svg_file, map_properties, all_layers=True):
        self.__svg = etree.parse(svg_file.get_fp())
        self.__map_properties = map_properties
        self.__all_layers = all_layers

    def clean(self):
    #===============
        self.__filter(self.__svg.getroot())

    def save(self, file_object):
    #===========================
        header = ' Generator: mapmaker {} at {} '.format(__version__, datetime.now(timezone.utc).isoformat())
        comments = self.__svg.xpath('/comment()')
        if len(comments):
            comments[0].text = header
        else:
            self.__svg.getroot().addprevious(etree.Comment(header))
        self.__svg.write(file_object, encoding='utf-8', pretty_print=True, xml_declaration=True)

    def __filter(self, element, parent=None):
    #========================================
        if self.__exclude(element):
            parent.remove(element)
            return
        for child in element:
            self.__filter(child, element)

    def __exclude(self, element):
    #============================
        if element.attrib.get('id', '').startswith('_x2E_'):
            markup = adobe_decode(element.attrib['id'])
            properties = self.__map_properties.update_feature_properties(parse_markup(markup))
            for key, value in properties.items():
                if key in EXCLUDE_SHAPE_TYPES:
                    return True
                elif not self.__all_layers and key == 'tile-layer' and value in EXCLUDE_TILE_LAYERS:
                    return True
        return False

#===============================================================================
