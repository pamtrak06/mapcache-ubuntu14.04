#!/usr/bin/python

import sys, getopt, logging
from owslib.wms import WebMapService


def main(argv):
    wmsUrl = ''
    project = ''
    
    logging.info('test')
    
    try:
        opts, args = getopt.getopt(argv,"w:p:",["wms=","prj="])
    except getopt.GetoptError:
        print 'mapcache.py -wms <wms url> -prj <project name>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'mapcache.py -wms <wms url> -prj <project name>'
            sys.exit()
        elif opt in ("-w", "-wms", "--wms"):
            wmsUrl = arg
        elif opt in ("-p", "-prj", "--prj"):
            project = arg
    
    logging.info('WMS url is "', wmsUrl)
    logging.info('Project name is "', project)

    wms = WebMapService(wmsUrl, version='1.1.1')
    #wms.identification.type
    #wms.identification.title

    mapcache = '';
    tileset = '';
    source = '';
    concat = '&amp;';
    urlRequestCapa = wmsUrl;
    idx = urlRequestCapa.index('?');
    if idx == -1:
        concat = '?';

    mapcache = '&lt;?xml version="1.0" encoding="UTF-8"?&gt;\n';
    mapcache += '&lt;mapcache&gt;\n';
    mapcache += '  &lt;metadata&gt;\n';
    mapcache += '    &lt;title&gt;Mapcache service for url: ' + urlRequestCapa + '&lt;/title&gt;\n';
    mapcache += '    &lt;abstract&gt;Render map services for url: ' + urlRequestCapa + '&lt;/abstract&gt;\n';
    mapcache += '  &lt;/metadata&gt;\n\n';

    # Cache: Disk
    mapcache += '  &lt;cache name="disk" type="disk"&gt;\n';
    mapcache += '    &lt;base&gt;/tmp/' + project + '&lt;/base&gt;\n';
    mapcache += '    &lt;symlink_blank/&gt;\n';
    mapcache += '  &lt;/cache&gt;\n\n';

    # Cache: template
    mapcache += '  &lt;cache name="tmpl" type="disk"&gt;\n';
    mapcache += '    &lt;base&gt;/tmp' + project + '&lt;/base&gt;\n';
    mapcache += '    &lt;template&gt;/tmp/' + project + '/template/{tileset}#{grid}#{dim}/{z}/{x}/{y}.{ext}&lt;/template&gt;\n';
    mapcache += '  &lt;/cache&gt;\n\n';

    # Cache: sqlite
    mapcache += '  &lt;cache name="sqlite" type="sqlite3"&gt;\n';
    mapcache += '    &lt;dbfile&gt;/tmp/' + project + '/sqlitetiles.db&lt;/dbfile&gt;\n';
    mapcache += '    &lt;pragma name="key"&gt;value&lt;/pragma&gt;\n';
    mapcache += '  &lt;/cache&gt;\n\n';

    # Cache: MbTiles
    mapcache += '  &lt;cache name="mbtiles" type="mbtiles"&gt;\n';
    mapcache += '    &lt;dbfile&gt;/tmp/' + project + '/' + project + '.mbtiles&lt;/dbfile&gt;\n';
    mapcache += '  &lt;/cache&gt;\n\n';

    # Format: png
    mapcache += '  &lt;format name="PNGQ_FAST" type ="PNG"&gt;\n';
    mapcache += '    &lt;compression&gt;fast&lt;/compression&gt;\n';
    mapcache += '    &lt;colors&gt;256&lt;/colors&gt;\n';
    mapcache += '  &lt;/format&gt;\n\n';

    # Format: jpeg
    mapcache += '  &lt;format name="JPEG_75" type ="JPEG"&gt;\n';
    mapcache += '    &lt;quality&gt;75&lt;/quality&gt;\n';
    mapcache += '    &lt;photometric&gt;RGB&lt;/photometric&gt;\n';
    mapcache += '  &lt;/format&gt;\n\n';

    # Format: png
    mapcache += '  &lt;format name="PNG_BEST" type ="PNG"&gt;\n';
    mapcache += '    &lt;compression&gt;best&lt;/compression&gt;\n';
    mapcache += '  &lt;/format&gt;\n\n';

    # Format: mixed
    mapcache += '  &lt;format name="mixed" type="MIXED"&gt;\n';
    mapcache += '    &lt;transparent&gt;PNG_BEST&lt;/transparent&gt;\n';
    mapcache += '    &lt;opaque&gt;JPEG&lt;/opaque&gt;\n';
    mapcache += '  &lt;/format&gt;\n\n';

    for layername in wms.contents:
        layer = wms.contents[layername];

        logging.info('Layer:' + layer.name);
        logging.info('\tAvailable elevations: '.join(layer.elevations));
        logging.info('\tAvailable times: '.join(layer.timepositions));

        arrayTab = layer.styles;
        for sname in arrayTab:
            style = arrayTab[sname];

            tileset = layer.name + '_' + sname;
            source = 'SOURCE_' + layer.name + '_' + sname;

            mapcache += '  &lt;!-- Source for layer: ' + layer.name + ', style: ' + sname + ' --&gt;\n';
            mapcache += '  &lt;source name="' + source + '" type="wms"&gt;\n';
            mapcache += '    &lt;http&gt;\n';
            mapcache += '      &lt;url&gt;' + urlRequestCapa + '&lt;/url&gt;\n';
            mapcache += '    &lt;/http&gt;\n';
            mapcache += '    &lt;getmap&gt;\n';
            mapcache += '      &lt;params&gt;\n';
            mapcache += '        &lt;FORMAT&gt;image/png&lt;/FORMAT&gt;\n';
            mapcache += '        &lt;LAYERS&gt;' + layer.name + '&lt;/LAYERS&gt;\n';
            mapcache += '        &lt;STYLES&gt;' + sname + '&lt;/STYLES&gt;\n';
            mapcache += '      &lt;/params&gt;\n';
            mapcache += '    &lt;/getmap&gt;\n';
            mapcache += '  &lt;/source&gt;\n\n';

            mapcache += '  &lt;!-- Tileset for layer: ' + layer.name + ', style: ' + sname + ' --&gt;\n';
            mapcache += '  &lt;tileset name="' + tileset + '"&gt;\n';
            mapcache += '    &lt;source&gt;' + source + '&lt;/source&gt;\n';
            mapcache += '    &lt;dimensions&gt;\n';
            mapcache += '      &lt;dimension type="regex" name="elevation" default="-1"&gt;.*&lt;/dimension&gt;\n';
            mapcache += '      &lt;dimension type="regex" name="time" default="' + layer.defaulttimeposition + '"&gt;.*&lt;/dimension&gt;\n';
            mapcache += '    &lt;/dimensions&gt;\n';
            mapcache += '    &lt;cache&gt;disk&lt;/cache&gt;\n';
            mapcache += '    &lt;format&gt;PNG&lt;/format&gt;\n';

            # TODO : create grid for each srs
            # projs = layer.srs;
            #for p in xrange(0, projs.length):
            #    proj = projs[p];
            #    mapcache += '    &lt;grid&gt;' + proj + '&lt;/grid&gt;\n';

            mapcache += '    &lt;grid&gt;WGS84&lt;/grid&gt;\n';
            mapcache += '    &lt;grid&gt;GoogleMapsCompatible&lt;/grid&gt;\n';
            mapcache += '    &lt;metatile&gt;5 5&lt;/metatile&gt;\n';
            mapcache += '    &lt;metabuffer&gt;10&lt;/metabuffer&gt;\n';
            mapcache += '  &lt;/tileset&gt;\n\n';


    # Services: wms
    mapcache += '  &lt;service type="wms" enabled="true"&gt;\n';
    for lname in wms.contents:
        layer = wms.contents[lname];
        arrayTab = layer.styles;
        for sname in arrayTab:
            style = arrayTab[sname];
            tileset = layer.name + '_' + sname;
            source = 'SOURCE_' + layer.name + '_' + sname;
            mapcache += '    &lt;forwarding_rule name="RULE' + tileset + '"&gt\n';
            mapcache += '      &lt;param name="SERVICE" type="values"&gt;WMS&lt;/param&gt\n';
            mapcache += '      &lt;param name="LAYERS" type="values"&gt;' + layer.name + '&lt;/param&gt\n';
            mapcache += '      &lt;param name="STYLES" type="values"&gt;' + sname + '&lt;/param&gt\n';
            mapcache += '      &lt;http&gt\n';
            mapcache += '        &lt;url&gt;' + urlRequestCapa + concat + 'LAYERS=' + tileset + '&lt;/url&gt\n';
            mapcache += '      &lt;/http&gt\n';
            mapcache += '    &lt;/forwarding_rule&gt\n';

    mapcache += '    &lt;full_wms&gt;assemble&lt;/full_wms&gt\n';
    mapcache += '    &lt;resample_mode&gt;bilinear&lt;/resample_mode&gt\n';
    mapcache += '    &lt;format&gt;JPEG_75&lt;/format&gt\n';
    mapcache += '    &lt;maxsize&gt;4096&lt;/maxsize&gt\n';
    mapcache += '  &lt;/service&gt\n\n';

    # Services: wmts, tms, gmaps, ve, demo
    mapcache += '  &lt;service type="wmts" enabled="true"/&gt;\n';
    mapcache += '  &lt;service type="tms" enabled="true"/&gt;\n';
    mapcache += '  &lt;service type="kml" enabled="true"/&gt;\n';
    mapcache += '  &lt;service type="gmaps" enabled="true"/&gt;\n';
    mapcache += '  &lt;service type="ve" enabled="true"/&gt;\n';
    mapcache += '  &lt;service type="demo" enabled="true"/&gt;\n\n';

    # General parameters
    mapcache += '  &lt;errors&gt;report&lt;/errors&gt;\n';
    mapcache += '  &lt;lock_dir&gt;/tmp/' + project + '&lt;/lock_dir&gt;\n';
    mapcache += '  &lt;threaded_fetching&gt;true&lt;/threaded_fetching&gt;\n';
    mapcache += '  &lt;log_level&gt;debug&lt;/log_level&gt;\n';
    mapcache += '  &lt;auto_reload&gt;true&lt/auto_reload&gt; \n';


    mapcache += '&lt;/mapcache&gt;\n';

    print mapcache;

if __name__ == "__main__":
   main(sys.argv[1:])
