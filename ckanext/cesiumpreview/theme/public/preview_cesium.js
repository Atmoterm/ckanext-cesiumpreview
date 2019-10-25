ckan.module('cesiumpreview', function (jQuery) {
    return {
        initialize: function () {

	    function items_csv (){
		return [{
		    "isEnabled"  : true,
		    "name": "costam", // name, 
		    "description": "niecostam", // description,
		    "type": 'csv',//format['type'],
		    "url": resource_url,
		    "tableStyle": {
			// "dataVariable": "State",
			// "timeColumn": null,
			// "scaleByValue": true,
			"scale": 1,
			// "colorMap": "green-orange-red",
			// "imageUrl": "/test/images/map-marker2.png"
		    }
		}]
	    }

	    // Generate generate WMS items for group category.  Parameter
	    // 'layer_title' defined in file 'ceisium.html', and contain
	    // zip-list of layers and titles names.  [['layer1', 'car'],
	    // ['layer2', 'towers']]
	    function items_wms (){
		var acc = [];
		format['layer_title'].forEach((layer_a_title) => acc.push(
		    {
			"isEnabled"  : true,
			"type"       : format['type'],
			"layers"     : layer_a_title[0],
			"name"       : layer_a_title[1],
			"description": description,
			"url"        : resource_url
		    }));
		return acc;
	    }

	    // 'camera' variable defined in file 'cesium.html'
	    function camera_position() {
		if  (!jQuery.isEmptyObject(format['camera']) &&
		     format['camera']['west' ] !== undefined  &&
		     format['camera']['south'] !== undefined  &&
		     format['camera']['east' ] !== undefined  &&
		     format['camera']['north'] !== undefined)
		{
		    console.log("TRUE");
		    return {
			'west'  : format['camera']['west' ],
			'south' : format['camera']['south'],
			'east'  : format['camera']['east' ],
			'north' : format['camera']['north'],
		    }
		}
		else
		{
		    // default format['camera'] to Poland
		    return {
			"north" : 54.87,
			"east"  : 24.1,
			"south" : 48.99,
			"west"  : 14.12,
		    }
		}
	    }

            var self = this;
	    var vis_server = 'https://dev-app.ekostrateg.com/mapy/#hideWorkbench=1&hideExplorerPanel=1';
            var config = {
                "version": "0.1",
		"hideSource": true,
                "initSources": [
                    {
                        initialCamera: {
			    "north" : 54.87,
			    "east"  : 24.1,
			    "south" : 48.99,
			    "west"  : 14.12,
			},
                        catalog: [
                            {
                                type: "group",
                                name: name,
                                isPromoted: true,
                                isOpen: true,
                                items: [],
                            }
                        ]
                    }
                ]
            };
	    
	    if (format["type"] == "wms") {
		config["initSources"][0]['initialCamera']        = camera_position();
		config["initSources"][0]['catalog'][0]['items']  = items_wms ();
	    }
	    if (format["type"] == "csv") {
		console.log(items_csv());
		config["initSources"][0]['catalog'][0]['items']  = items_csv ();
	    }

	    console.log(config);
            var encoded_config = encodeURIComponent(JSON.stringify(config));
            var style = 'height: 600px; width: 100%; border: none;';
            var display = 'allowFullScreen mozAllowFullScreen webkitAllowFullScreen';
            var html = '<iframe src="' + vis_server + '#clean&start=' + encoded_config + '" style="' + style + '" ' + display + '></iframe>';
            self.el.html(html);
        }
    };
});
