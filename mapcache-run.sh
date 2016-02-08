#!/bin/sh

# ---------------------------------------------------------------------------
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
# ---------------------------------------------------------------------------

url=$1
cache=$2

if [ $# -eq 0 ]
  then

    echo 'ERROR : no arguments supplied'
    echo 'mapcache-run --wms \"wms url\" --prj \"folder name for cache\"'

  else
    if [ -z "$1" ] || [ -z "$2" ]
      then

        echo 'ERROR : argument(s) could not be empty'
        echo 'mapcache-run --wms \"wms url\" --prj \"folder name for cache\"'

      else

        # generate mapcache.xml from capabilities
        python mapcache.py --wms $url --prj $cache

        # Create temp directory for mapcache tiles
        if [ ! -d "/tmp/$cache" ]; then
          mkdir /tmp/$cache
          chmod 755 /tmp/$cache
        fi

        # restart apache and mapcache module
        apachectl stop; apachectl start;

    fi
fi
