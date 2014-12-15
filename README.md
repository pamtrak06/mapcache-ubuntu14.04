# What is mapcache ?

"MapCache is a server that implements tile caching to speed up access to WMS layers. The primary objectives are to be fast and easily deployable, while offering the essential features (and more!) expected from a tile caching solution." > [Source](http://www.mapserver.org/mapcache/)

![logo](http://www.mapserver.org/_static/banner.png)
> [Slideshare](http://fr.slideshare.net/tbonfort/modgeocache-mapcache-a-fast-tiling-solution-for-the-apache-web-server)

# How to use this image

## build mapcache instance

### for ubuntu:utopic & apache2
docker build -t pamtrak06/mapcache:latest https://raw.githubusercontent.com/pamtrak06/mapcache/master/docker-ubuntu-utopic-apache2/Dockerfile

### for ubuntu:utopic & nodejs (under construction)
~~docker build -t pamtrak06/mapcache:latest~~ ~~https://raw.githubusercontent.com/pamtrak06/mapcache/master/docker-ubuntu-utopic-nodejs/Dockerfile~~

## Run Mapcache

Boot docker
```
$ boot2docker start
```

Run container
```
docker run -i -t -p 80:80 pamtrak06/ubuntu-utopic-mapcache2
$ apachectl start
```

get docker vm ip : 
```
$ boot2Docker ip => 192.168.59.103
```

GetCapabilities
```
http://192.168.59.103/mapcache/wmts/?service=wmts&request=getCapabilities
```

GetTile
```
http://192.168.59.103/mapcache/wmts/?service=WMTS&request=GetTile&format=image/png&width=1600&height=600&srs=EPSG:4326&layer=GDPS.ETA_P0_PRESSURE&TileMatrixSet=WGS84&TileMatrix=0&TileRow=0&TileCol=0&time=2014-12-09T06:00:00Z

http://192.168.59.103/mapcache/wmts/?service=WMTS&request=GetTile&format=image/png&width=1600&height=600&srs=EPSG:4326&layer=GDPS.ETA_P0_PRESSURE&TileMatrixSet=WGS84&TileMatrix=0&TileRow=0&TileCol=1&time=2014-12-09T06:00:00Z
```

![ScreenShot](https://github.com/pamtrak06/mapcache/blob/master/geometca0.png)![ScreenShot](https://github.com/pamtrak06/mapcache/blob/master/geometca1.png)

## Configure container
Mapcache configuration file could be fully modified or replaced
```
$ vi /etc/apache2/conf-available/mapcache.xml
```
with help from http://mapserver.org/fr/mapcache/config.html,
and then after modification restart apache server like
```
$ apachectl restart
```

Take care about mapcache cache strategy (with type="disk" all is stored in container)

Mapcache configuration file could be built from python script mapcache.py, arguments are :
```
$  python mapcache.py -wms <wms url> -prj <project name>
```
Example :
```
$  python mapcache.py --wms http://geo.weather.gc.ca/geomet/?lang=E --prj geometca
```
