import xml.etree.ElementTree as ET
from ckan.common import json
try:
    import os
    import ckanext.resourceproxy.plugin as proxy
    import requests
except ImportError:
    pass



class CSV(object):
    def type(self):
        return 'csv'


class GeoJSON(object):
    def type(self):
        return 'geojson'    



class WMS(object):
    _xml = None
    _xml_root = None
    _layers = None
    _titles = None
    _camera = None
    _layers_titles = None
    
    def __init__(self, url=None):
        if not url == None:
            self._xml      = requests.get(url).text.encode('utf-8').strip()
            self._xml_root = ET.fromstring(self._xml)

    def __valid__(self):
        return not self._xml_root == None
    
    def ValidWMS(func):
        def wrapper(self, *args, **kwargs):
            if not self.__valid__():
                return self
            else:
                return func(self, *args, **kwargs);
        return wrapper
    
    @ValidWMS
    def wms_layers(self):
        self._layers = [layer_name.text
                           for layer       in self._xml_root.iter("Layer")
                           for layer_name  in layer.findall("./Name")]
        return self


    @ValidWMS
    def wms_titles(self):
        self._titles = [title_name.text
                        for title       in self._xml_root.iter("Layer")
                        for title_name  in title.findall("./Layer/Title")]
        return self

    
    @ValidWMS
    def wms_titles_layers(self):
        if self._layers == None: self.wms_layers()
        if self._titles == None: self.wms_titles()
        if (len(self._layers) == len(self._titles)) or (len(self._layers) < len(self._titles)):
            self._layers_titles = list(zip(self._layers, self._titles))
            return self
        if (len(self._layers) > len(self._titles)):
            clayers = len(self._layers)
            ctitles = len(self._titles)
            titles  = titles + self._layers[ctitles:clayers]
            self._layers_titles = list(zip(self._layers, titles))
        return self


    @ValidWMS
    def wms_camera(self):
        LatLonBoundingBox = self._xml_root.findall("Capability/Layer/LatLonBoundingBox")[0]
        self._camera = { 'north' : LatLonBoundingBox.attrib["maxy"] ,
                         'east'  : LatLonBoundingBox.attrib["maxx"] ,
                         'south' : LatLonBoundingBox.attrib["miny"] ,
                         'west'  : LatLonBoundingBox.attrib["minx"] }
        print(self._camera)
        return self
    
    def wms_all(self):
        self.wms_layers()
        self.wms_camera()
        self.wms_titles_layers()
        return self

    def layers(self):
        if self._layers == None:
            return json.dumps([])
        else:
            return json.dumps(self._layers)

    def camera(self):
        if self._camera == None:
            return json.dumps({});
        else:
            return json.dumps(self._camera);

    def layers_titles(self):
        if self._layers_titles == None:
            return json.dumps([])
        else:
            return json.dumps(self._layers_titles);
        

    def type(self):
        return 'wms'


