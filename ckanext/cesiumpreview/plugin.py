import logging
import ckan.plugins as p
import ckan.model as model
from ckan.common import json
from ckan.plugins.toolkit import get_action, ObjectNotFound, NotAuthorized
from formats import WMS, CSV, GeoJSON
try:
    import os
    import ckanext.resourceproxy.plugin as proxy
    import requests
except ImportError:
    pass

log = logging.getLogger(__name__)

        

class CesiumPreview(p.SingletonPlugin):
    ''' Cesium WMS view '''
    
    ''' INTERFACES '''
    p.implements(p.IConfigurer,   inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IResourceView, inherit=True)
    p.implements(p.ITemplateHelpers, inherit=True)

    ''' PARAMS '''
    _cesium_formats = ['wms', 'csv', 'geojson', 'gjson']
    _proxy_is_enabled = False


    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_resource('theme/public', 'ckanext-cesiumpreview')

    def configure(self, config):
        enabled = config.get('ckan.resource_proxy_enabled', False)
        self._proxy_is_enabled = enabled

    def can_preview(self, data_dict):
        resource = data_dict['resource']
        format_lower = resource['format'].lower()
        if (format_lower == ''):
            format_lower = os.path.splitext(resource['url'])[1][1:].lower()
        if format_lower in self._cesium_formats:
            if resource.get('on_same_domain') or self._proxy_is_enabled:
                return {'can_preview': True, 'quality': 2}
            else:
                return {'can_preview': True,
                        'fixable': 'Enable resource_proxy',
                        'quality': 2}
        return {'can_preview': False}

    def info(self):
        return {
            'name': 'cesium_view',
            'title': 'Cesium Map View',
            'always_available': True,
            'default_title': 'Cesium Map View',
            'icon': 'globe' }

    def can_view(self, data_dict):
        resource = data_dict['resource']
        format_lower = resource.get('format', '').lower()
        if (format_lower == ''):
            format_lower = os.path.splitext(resource['url'])[1][1:].lower()
        if format_lower in self._cesium_formats:
	    return True
        return False

    def setup_template_variables(self, context, data_dict):
        if (self._proxy_is_enabled
            and not data_dict['resource']['on_same_domain']):
            url = proxy.get_proxified_resource_url(data_dict)
            p.toolkit.c.resource['url'] = url

    def setup_template_variables(self, context, data_dict):
        print("DUPAdddddd: ")
        print(data_dict['resource'])
        return {'resource_json'     : json.dumps(data_dict['resource']),
                'resource_view_json': json.dumps(data_dict['resource_view'])}

    def preview_template(self, context, data_dict):
        return 'cesium.html'

    def view_template(self, context, data_dict):
        return 'cesium.html'

    def get_helpers(self):
        return { 'resource_show':  self.resource_show,
                 'load_geodata':  self.load_geodata}

    '''WMS resource parser and helper function'''
    def load_geodata(self, data_dict):
        resource = self.resource_show({'model': model, 'ignore_auth': True}, data_dict)
        resource_format = resource[u'format'].lower().strip()
        
        if resource_format == 'wms': return WMS(resource[u"url"]).wms_all()
        if resource_format == 'csv': return CSV()
        if resource_format == 'gjson' or resource_format == 'geojson': return GeoJSON()
        
        return WMS()

    def resource_show(self, context, data_dict):
        return get_action('resource_show')(context, data_dict)


'''
# example of resource data
{
   'mimetype':None,
   'cache_url':None,
   'hash':'',
   'description':'',
   'name':'dyrekcja costam',
   'format':'WMS',
   'url':'https://dev-app.ekostrateg.com/cgeoserver/Luma/wms?version=1.1.1&service=WMS&request=GetCapabilities',
   'datastore_active':False,
   'cache_last_updated':None,
   'package_id':'01be2195-390d-46cc-b99f-df2af4dcc7b1',
   'created':'2019-10-10T12:31:30.662767',
   'state':'active',
   'mimetype_inner':None,
   'last_modified':None,
   'position':0,
   'revision_id':'ab75d171-b2b3-4636-9304-f69ab2fb13e5',
   'url_type':'',
   'id':'09d21bf0-c2f3-4b7b-a514-51f11cb7117a',
   'resource_type':None,
   'size':None
}

'''
