mapcache
========

ubuntu &amp; mapcache

## build mapcache 

### for ubuntu:utopic & apache2
docker build -t pamtrak06/mapcache:latest https://raw.githubusercontent.com/pamtrak06/mapcache/master/docker-ubuntu-utopic-apache2/Dockerfile

### for ubuntu:utopic & nodejs
-- ON WORK --
docker build -t pamtrak06/mapcache:latest https://raw.githubusercontent.com/pamtrak06/mapcache/master/docker-ubuntu-utopic-nodejs/Dockerfile

## Get capabilities/ get tile

Run docker
  '''docker run -i -t -p 80:80 pamtrak06/ubuntu-utopic-mapcache2'''

get docker vm ip : 
   '''boot2Docker ip => 192.168.59.103'''

GetCapabilities
   '''http://192.168.59.103/mapcache/wmts/?service=wmts&request=getCapabilities'''

GetTile
   '''http://192.168.59.103/mapcache/wmts/?service=WMTS&request=GetTile&format=image/png&width=1600&height=600&srs=EPSG:4326&layer=GDPS.ETA_P0_PRESSURE&TileMatrixSet=WGS84&TileMatrix=0&TileRow=0&TileCol=0&time=2014-12-09T06:00:00Z'''
