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
    _terria_map_server= ''


    def update_config(self, config):
        p.toolkit.add_public_directory(config, 'theme/public')
        p.toolkit.add_template_directory(config, 'theme/templates')
        p.toolkit.add_resource('theme/public', 'ckanext-cesiumpreview')

    def configure(self, config):
        enabled = config.get('ckan.resource_proxy_enabled', False)
        self._proxy_is_enabled = enabled
	self._terria_map_server = config.get('ckan.terria.server', 'https://nationalmap.gov.au/')
	if (self._terria_map_server[len(self._terria_map_server)-1] == '/'):
		self._terria_map_server = self._terria_map_server.strip() + "#mode=preview&map=2d&hideWorkbench=1&hideExplorerPanel=1"
	else:
		self._terria_map_server = self._terria_map_server.strip() + "/#mode=preview&map=2d&hideWorkbench=1&hideExplorerPanel=1"

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
        return {'resource_json'     : json.dumps(data_dict['resource']),
                'resource_view_json': json.dumps(data_dict['resource_view']),
                'terria_server'     : self._terria_map_server}

    def preview_template(self, context, data_dict):
        return 'cesium.html'

    def view_template(self, context, data_dict):
        return 'cesium.html'

    def get_helpers(self):
        return { 'resource_show':  self.resource_show,
                 'load_geodata' :  self.load_geodata }

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

