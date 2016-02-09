#!/usr/bin/python

# ---------------------------------------------------------------------------
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# ---------------------------------------------------------------------------

from __future__ import unicode_literals
import sys, getopt, logging
from owslib.wms import WebMapService
from xml.etree import ElementTree as ET
from xml.sax.saxutils import unescape

def main(argv):
    wmsUrl = u"";
    project = u"";
    
    try:
        opts, args = getopt.getopt(argv,"w:p:",["wms=","prj="])
    except getopt.GetoptError:
        print "mapcache.py -wms <wms url> -prj <project name>";
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "mapcache.py -wms <wms url> -prj <project name>";
            sys.exit();
        elif opt in ("-w", "-wms", "--wms"):
            wmsUrl = arg;
        elif opt in ("-p", "-prj", "--prj"):
            project = arg;

    #logging.info(u"WMS url is ", wmsUrl);
    #logging.info(u"Project name is ", project);

    wms = WebMapService(wmsUrl, version=u"1.1.1")
    #wms.identification.type
    #wms.identification.title

    mapcache = u"";
    tileset = u"";
    source = u"";
    concat = u"&amp;";
    urlRequestCapa = wmsUrl;
    idx = urlRequestCapa.index(u"?");
    if idx == -1:
        concat = u"?";

    mapcache = u"&lt;?xml version=\"1.0\" encoding=\"UTF-8\"?&gt;\n";
    mapcache += u"&lt;mapcache&gt;\n";
    mapcache += u"  &lt;metadata&gt;\n";
    mapcache += u"    &lt;title&gt;Mapcache service for url: " + urlRequestCapa + u"&lt;/title&gt;\n";
    mapcache += u"    &lt;abstract&gt;Render map services for url: " + urlRequestCapa + u"&lt;/abstract&gt;\n";
    mapcache += u"  &lt;/metadata&gt;\n\n";

    # Cache: Disk
    mapcache += u"  &lt;cache name=\"disk\" type=\"disk\"&gt;\n";
    mapcache += u"    &lt;base&gt;/tmp/" + project + u"&lt;/base&gt;\n";
    mapcache += u"    &lt;symlink_blank/&gt;\n";
    mapcache += u"  &lt;/cache&gt;\n\n";

    # Cache: template
    mapcache += u"  &lt;cache name=\"tmpl\" type=\"disk\"&gt;\n";
    mapcache += u"    &lt;base&gt;/tmp" + project + u"&lt;/base&gt;\n";
    mapcache += u"    &lt;template&gt;/tmp/" + project + u"/template/{tileset}#{grid}#{dim}/{z}/{x}/{y}.{ext}&lt;/template&gt;\n";
    mapcache += u"  &lt;/cache&gt;\n\n";

    # Cache: sqlite
    mapcache += u"  &lt;cache name=\"sqlite\" type=\"sqlite3\"&gt;\n";
    mapcache += u"    &lt;dbfile&gt;/tmp/" + project + u"/sqlitetiles.db&lt;/dbfile&gt;\n";
    mapcache += u"    &lt;pragma name=\"key\"&gt;value&lt;/pragma&gt;\n";
    mapcache += u"  &lt;/cache&gt;\n\n";

    # Cache: MbTiles
    mapcache += u"  &lt;cache name=\"mbtiles\" type=\"mbtiles\"&gt;\n";
    mapcache += u"    &lt;dbfile&gt;/tmp/" + project + u"/" + project + u".mbtiles&lt;/dbfile&gt;\n";
    mapcache += u"  &lt;/cache&gt;\n\n";

    # Format: png
    mapcache += u"  &lt;format name=\"PNGQ_FAST\" type =\"PNG\"&gt;\n";
    mapcache += u"    &lt;compression&gt;fast&lt;/compression&gt;\n";
    mapcache += u"    &lt;colors&gt;256&lt;/colors&gt;\n";
    mapcache += u"  &lt;/format&gt;\n\n";

    # Format: jpeg
    mapcache += u"  &lt;format name=\"JPEG_75\" type =\"JPEG\"&gt;\n";
    mapcache += u"    &lt;quality&gt;75&lt;/quality&gt;\n";
    mapcache += u"    &lt;photometric&gt;RGB&lt;/photometric&gt;\n";
    mapcache += u"  &lt;/format&gt;\n\n";

    # Format: png
    mapcache += u"  &lt;format name=\"PNG_BEST\" type =\"PNG\"&gt;\n";
    mapcache += u"    &lt;compression&gt;best&lt;/compression&gt;\n";
    mapcache += u"  &lt;/format&gt;\n\n";

    # Format: mixed
    mapcache += u"  &lt;format name=\"mixed\" type=\"MIXED\"&gt;\n";
    mapcache += u"    &lt;transparent&gt;PNG_BEST&lt;/transparent&gt;\n";
    mapcache += u"    &lt;opaque&gt;JPEG&lt;/opaque&gt;\n";
    mapcache += u"  &lt;/format&gt;\n\n";

    for layername in wms.contents:
        layer = wms.contents[layername];

        #logging.info("Layer:" + layer.name);
        #logging.info("\tAvailable elevations: ".join(layer.elevations));
        #logging.info("\tAvailable times: ".join(layer.timepositions));

        arrayTab = layer.styles;
        for sname in arrayTab:
            style = arrayTab[sname];

            tileset = layer.name + u"_" + sname;
            source = u"SOURCE_" + layer.name + u"_" + sname;

            mapcache += u"  &lt;!-- Source for layer: " + layer.name + u", style: " + sname + u" --&gt;\n";
            mapcache += u"  &lt;source name=\"" + source + u"\" type=\"wms\"&gt;\n";
            mapcache += u"    &lt;http&gt;\n";
            mapcache += u"      &lt;url&gt;" + urlRequestCapa + u"&lt;/url&gt;\n";
            mapcache += u"    &lt;/http&gt;\n";
            mapcache += u"    &lt;getmap&gt;\n";
            mapcache += u"      &lt;params&gt;\n";
            mapcache += u"        &lt;FORMAT&gt;image/png&lt;/FORMAT&gt;\n";
            mapcache += u"        &lt;LAYERS&gt;" + layer.name + u"&lt;/LAYERS&gt;\n";
            mapcache += u"        &lt;STYLES&gt;" + sname + u"&lt;/STYLES&gt;\n";
            mapcache += u"      &lt;/params&gt;\n";
            mapcache += u"    &lt;/getmap&gt;\n";
            mapcache += u"  &lt;/source&gt;\n\n";

            mapcache += u"  &lt;!-- Tileset for layer: " + layer.name + u", style: " + sname + u" --&gt;\n";
            mapcache += u"  &lt;tileset name=\"" + tileset + u"\"&gt;\n";
            mapcache += u"    &lt;source&gt;" + source + u"&lt;/source&gt;\n";
            mapcache += u"    &lt;dimensions&gt;\n";
            #mapcache += u"      &lt;dimension type=\"regex\" name=\"elevation\" default=\"-1\"&gt;.*&lt;/dimension&gt;\n";
            mapcache += u"      &lt;dimension type=\"time\" name=\"time\" default=\"" + layer.defaulttimeposition + u"\"&gt;.*&lt;/dimension&gt;\n";
            mapcache += u"    &lt;/dimensions&gt;\n";
            mapcache += u"    &lt;cache&gt;disk&lt;/cache&gt;\n";
            mapcache += u"    &lt;format&gt;PNG&lt;/format&gt;\n";

            # TODO : create grid for each srs
            # projs = layer.srs;
            #for p in xrange(0, projs.length):
            #    proj = projs[p];
            #    mapcache += u"    &lt;grid&gt;" + proj + u"&lt;/grid&gt;\n";

            mapcache += u"    &lt;grid&gt;WGS84&lt;/grid&gt;\n";
            mapcache += u"    &lt;grid&gt;GoogleMapsCompatible&lt;/grid&gt;\n";
            mapcache += u"    &lt;metatile&gt;5 5&lt;/metatile&gt;\n";
            mapcache += u"    &lt;metabuffer&gt;10&lt;/metabuffer&gt;\n";
            mapcache += u"  &lt;/tileset&gt;\n\n";


    # Services: wms
    mapcache += u"  &lt;service type=\"wms\" enabled=\"true\"&gt;\n";
    for lname in wms.contents:
        layer = wms.contents[lname];
        arrayTab = layer.styles;
        for sname in arrayTab:
            style = arrayTab[sname];
            tileset = layer.name + u"_" + sname;
            source = u"SOURCE_" + layer.name + u"_" + sname;
            mapcache += u"    &lt;forwarding_rule name=\"RULE" + tileset + u"\"&gt;\n";
            mapcache += u"      &lt;param name=\"SERVICE\" type=\"values\"&gt;WMS&lt;/param&gt;\n";
            mapcache += u"      &lt;param name=\"LAYERS\" type=\"values\"&gt;" + layer.name + u"&lt;/param&gt;\n";
            mapcache += u"      &lt;param name=\"STYLES\" type=\"values\"&gt;" + sname + u"&lt;/param&gt;\n";
            mapcache += u"      &lt;http&gt;\n";
            mapcache += u"        &lt;url&gt;" + urlRequestCapa + concat + u"LAYERS=" + tileset + u"&lt;/url&gt;\n";
            mapcache += u"      &lt;/http&gt;\n";
            mapcache += u"    &lt;/forwarding_rule&gt;\n";

    mapcache += u"    &lt;full_wms&gt;assemble&lt;/full_wms&gt;\n";
    mapcache += u"    &lt;resample_mode&gt;bilinear&lt;/resample_mode&gt;\n";
    mapcache += u"    &lt;format&gt;JPEG_75&lt;/format&gt;\n";
    mapcache += u"    &lt;maxsize&gt;4096&lt;/maxsize&gt;\n";
    mapcache += u"  &lt;/service&gt;\n\n";

    # Services: wmts, tms, gmaps, ve, demo
    mapcache += u"  &lt;service type=\"wmts\" enabled=\"true\"/&gt;\n";
    mapcache += u"  &lt;service type=\"tms\" enabled=\"true\"/&gt;\n";
    mapcache += u"  &lt;service type=\"kml\" enabled=\"true\"/&gt;\n";
    mapcache += u"  &lt;service type=\"gmaps\" enabled=\"true\"/&gt;\n";
    mapcache += u"  &lt;service type=\"ve\" enabled=\"true\"/&gt;\n";
    mapcache += u"  &lt;service type=\"demo\" enabled=\"true\"/&gt;\n\n";

    # General parameters
    mapcache += u"  &lt;errors&gt;report&lt;/errors&gt;\n";
    mapcache += u"  &lt;lock_dir&gt;/tmp/" + project + u"&lt;/lock_dir&gt;\n";
    mapcache += u"  &lt;threaded_fetching&gt;true&lt;/threaded_fetching&gt;\n";
    mapcache += u"  &lt;log_level&gt;debug&lt;/log_level&gt;\n";
    mapcache += u"  &lt;auto_reload&gt;true&lt;/auto_reload&gt; \n";


    mapcache += u"&lt;/mapcache&gt;\n";

    escmapcache = unescape(mapcache);
    #print escmapcache;
    #fmapcache = ET.fromstring(ET.tostring(escmapcache.encode("utf8"), method="xml"));
    #tree = ET.XML(escmapcache.encode("utf8"));
    with open("mapcache.xml", "w") as f:
        #f.write(ET.tostring(tree))
        f.write(escmapcache)

if __name__ == "__main__":
   main(sys.argv[1:])
