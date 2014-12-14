# Model from https://github.com/geo-data/node-mapcache
#
# This creates an Ubuntu derived base image that installs a recent
# version of Apache as well as the latest repository checkouts of
# Mapserver Mapcache. Mapcache has a
# broad range of compile time options enabled and as such this
# provides a suitable base image for both experimenting with and
# deriving production ready images from.
#

FROM ubuntu:14.04

MAINTAINER pamtrak06 <pamtrak06@gmail.com>

# Ensure the package repository is up to date
#RUN echo "deb http://fr.archive.ubuntu.com/ubuntu utopic main universe" > /etc/apt/sources.list
#RUN echo "deb http://ppa.launchpad.net/smartlounge/ppa/ubuntu utopic main universe" >> /etc/apt/sources.list
RUN echo "deb http://ppa.launchpad.net/kubuntu-ppa/backports/ubuntu trusty-security main restricted" >> /etc/apt/sources.list

# Take account about PUBKEY
#RUN apt-get update &> apt-get_update.log
#RUN more apt-get_update.log | grep NO_PUBKEY | awk -F 'NO_PUBKEY ' '{print $2}' > PUBKEY.txt
#RUN rm -f apt-get_update.log
#ENV PUBKEY=`more PUBKEY.txt`
#RUN rm -f PUBKEY.txt
#RUN sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com $PUBKEY
#RUN unset PUBKEY
# Update os
RUN sudo apt-get update

# Install Apache
RUN apt-get install -y apache2

# Configure localhost
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf

# Install mapcache compilation prerequisites
RUN apt-get install -y software-properties-common python-software-properties python g++ make cmake

# Install mapcache dependencies provided by Ubuntu repositories
RUN apt-get install -y git \
    libaprutil1-dev \
    libapr1-dev \
    libpng12-dev \
    libjpeg-dev \
    libcurl4-gnutls-dev \
    libpcre3-dev \
    libpixman-1-dev \
    libgdal-dev \
    libgeos-dev \
    libsqlite3-dev \
    libdb-dev \
    libtiff-dev

# Install Mapcache itself
RUN git clone https://github.com/mapserver/mapcache/ /usr/local/src/mapcache
# Setting Apache2 environment variables
RUN source /etc/apache2/envvars
# Erase mapcache build folder
RUN rm -rf /usr/local/src/mapcache/build
# Resolve Could NOT find APACHE (missing:  APACHE_INCLUDE_DIR) / APACHE library/component could not be found and is a mandatory dependency
#RUN sudo apt-cache search apache2|grep -i devel
RUN sudo apt-get install apache2-threaded-dev
# Compile Mapcache for Apache
RUN mkdir /usr/local/src/mapcache/build && \
    cd /usr/local/src/mapcache/build && \
    cmake ../ -DWITH_FCGI=0 -DWITH_APACHE=1 -DWITH_PCRE=1 -DWITH_TIFF=1 -DWITH_BERKELEY_DB=1 -DWITH_MEMCACHE=1 -DCMAKE_PREFIX_PATH="/etc/apache2" && \
    make && \
    make install

# Apache2 configuration for mapcache
RUN echo "LoadModule mapcache_module    /usr/lib/apache2/modules/mod_mapcache.so" > /etc/apache2/mods-available/mapcache.load

RUN echo "<IfModule mapcache_module>" > /etc/apache2/mods-available/mapcache.conf
RUN echo "   <Directory /etc/apache2/conf-available>" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "      Require all granted" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "   </Directory>" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "   MapCacheAlias /mapcache \"/etc/apache2/conf-available/mapcache.xml\"" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "</IfModule>" >> /etc/apache2/mods-available/mapcache.conf

# Enable mapcache module
RUN a2enmod mapcache

# Install an javascript interpreter (V8 from chromium)
#RUN sudo apt-get install subversion scons libreadline-dev
#RUN cd /usr/local/src
#RUN svn co http://v8.googlecode.com/svn/trunk v8
#RUN cd v8/
#RUN make builddeps
#RUN make native console=readline
#RUN scons console=readline d8

# Download javascript to build mapcache.xml
#RUN cd /var/www/html
#RUN curl -O http://pamtrak06.github.io/jquery.min.js
#RUN curl -O http://pamtrak06.github.io/addons/xml.js
#RUN curl -O http://pamtrak06.github.io/ol.js
#RUN curl -O http://pamtrak06.github.io/mapPower/mapcache.js
# Execute javascript to build mapcache.xml with ENTRYPOINT wms/url parameter
# TBD : execute javascript ...
#RUN cd /etc/apache2/conf-available
#RUN cp /var/www/html/mapcache.xml .

# Install pip
RUN apt-get install python-pip
# Install OGC library
RUN pip install OWSLib
# Set path for mapcache file
RUN cd /etc/apache2/conf-available/
# Download py library to produce mapcache.xml from a wms url
RUN curl -O https://raw.githubusercontent.com/pamtrak06/mapcache/master/mapcache.py
# Generate mapcache.xml sample
RUN python mapcache.py --wms http://geo.weather.gc.ca/geomet/?lang=E --prj mapcache

# Download example 
#RUN curl -O https://raw.githubusercontent.com/pamtrak06/mapcache/master/mapcache.xml

# Create temp directory for mapcache tiles
RUN rm -rf /tmp/mapcache
RUN mkdir /tmp/mapcache
RUN chmod 777 /tmp/mapcache

# start apache
RUN apachectl start

#EXPOSE 80
#VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
#ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

# test
# curl http://localhost/mapcache/demo

# Install Firefox
#RUN apt-get install -y firefox
