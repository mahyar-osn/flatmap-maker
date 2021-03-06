#===============================================================================
#
#  Flatmap viewer and annotation tools
#
#  Copyright (c) 2020  David Brooks
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

import io
import json
import pathlib
import urllib.request

#===============================================================================

# Export from module

from .logging import ProgressBar, log

#===============================================================================

class FilePath(object):
    def __init__(self, path):
        if (path.startswith('file:')
         or path.startswith('http:')
         or path.startswith('https:')):
            self.__url = path
        else:
            self.__url = pathlib.Path(path).absolute().as_uri()

    @property
    def url(self):
        return self.__url

    def close(self):
        self.__fp.close()

    def get_data(self):
        with self.get_fp() as fp:
            return fp.read()

    def get_fp(self):
        return urllib.request.urlopen(self.__url)

    def get_json(self):
        try:
            return json.loads(self.get_data())
        except json.decoder.JSONDecodeError as err:
            raise ValueError('JSON decoder error: {}'.format(err))

    def get_BytesIO(self):
        bytesio = io.BytesIO(self.get_data())
        bytesio.seek(0)
        return bytesio

#===============================================================================
