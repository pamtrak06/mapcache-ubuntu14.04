# Model from https://github.com/geo-data/node-mapcache
#
# This creates an Ubuntu derived base image that installs a recent
# version of Apache as well as the latest repository checkouts of
# Mapserver Mapcache. Mapcache has a
# broad range of compile time options enabled and as such this
# provides a suitable base image for both experimenting with and
# deriving production ready images from.
#

FROM ubuntu:utopic

MAINTAINER pamtrak06 <pamtrak06@gmail.com>

# Ensure the package repository is up to date
RUN echo "deb http://fr.archive.ubuntu.com/ubuntu utopic main universe" > /etc/apt/sources.list
RUN echo "deb http://ppa.launchpad.net/smartlounge/ppa/ubuntu utopic main universe" >> /etc/apt/sources.list
RUN apt-get update

# Install compilation prerequisites
RUN apt-get install -y software-properties-common python-software-properties python g++ make cmake
RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get install -y nodejs


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
# Erase mapcache build folder
RUN rm -rf /usr/local/src/mapcache/build
# Compile Mapcache for Apache
RUN mkdir /usr/local/src/mapcache/build && \
    cd /usr/local/src/mapcache/build && \
    cmake ../ -DWITH_FCGI=0 -DWITH_APACHE=0 -DWITH_PCRE=1 -DWITH_TIFF=1 -DWITH_BERKELEY_DB=1 -DWITH_MEMCACHE=1 -DCMAKE_PREFIX_PATH="/etc/apache2" && \
    make && \
    make install

RUN npm config set mapcache:build_dir /usr/local/src/mapcache/build && \
    npm install /usr/local/src/node-mapcache


# Download mapcache.xml
RUN cd /etc/apache2/conf-available
RUN curl -O https://raw.githubusercontent.com/pamtrak06/mapcache/master/mapcache.xml

# Create temp directory for mapcache tiles
RUN rm -rf /tmp/geometca
RUN mkdir /tmp/geometca
RUN chmod 777 /tmp/geometca/

# Configure localhost
# TBD

# Run the Node Mapcache tests by default
CMD npm test mapcache

