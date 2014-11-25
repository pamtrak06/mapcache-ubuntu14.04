# Model from https://github.com/geo-data/node-mapcache
#
# This creates an Ubuntu derived base image that installs a recent
# version of Node.js as well as the latest repository checkouts of
# Mapserver Mapcache and the Node Mapcache bindings.  Mapcache has a
# broad range of compile time options enabled and as such this
# provides a suitable base image for both experimenting with and
# deriving production ready images from.
#

FROM ubuntu:lucid

MAINTAINER pamtrak06 <pamtrak06@gmail.com>

# Ensure the package repository is up to date
RUN echo "deb http://fr.archive.ubuntu.com/ubuntu lucid main universe" > /etc/apt/sources.list
RUN echo "deb http://ppa.launchpad.net/smartlounge/ppa/ubuntu hardy main" >> /etc/apt/sources.list
RUN apt-get update

# Install Node.js
RUN apt-get update
RUN apt-get install -y software-properties-common python-software-properties python g++ make cmake
RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get install -y nodejs


# libapr1-dev dependencies
RUN apt-get install -y uuid-dev
# libaprutil1-dev dependencies
RUN apt-get install -y libldap2-dev \
    libexpat1-dev \
    libpq-dev \
    libmysqlclient-dev
# libcurl4-gnutls-dev dependencies
RUN apt-get install -y libcurl3-gnutls \
    libc6-dev \
    libc-dev \
    libgnutls-dev \
    zlib1g-dev \
    libkrb5-dev \
    hurd \
    libldap2-dev
# libgdal1-dev dependencies
RUN apt-get install -y libgdal1-1.6.0 \
    libc6-dev \
    libhdf4-alt-dev \
    libpq-dev but \
    libxerces-c2-dev \
    libmysqlclient-dev \
    libhdf5-serial-dev
#libjpeg62-dev : Depends: libc-dev
#libpcre3-dev : Depends: libc6-dev but it is not going to be installed
#               Depends: libpcre3 (= 7.8-3build1) but 1:8.35-3ubuntu1 is to be installed
#libpng12-dev : Depends: libpng12-0 (= 1.2.42-1ubuntu2) but 1.2.51-0ubuntu3 is to be installed
#               Depends: zlib1g-dev but it is not going to be installed
#libsqlite3-dev : Depends: libsqlite3-0 (= 3.6.22-1) but 3.8.6-1 is to be installed
#                 Depends: libc6-dev but it is not going to be installed
#libtiff4-dev : Depends: libc6-dev but it is not going to be installed or
#                       libc-dev
#              Depends: zlib1g-dev but it is not going to be installed
# Install mapcache dependencies provided by Ubuntu repositories
RUN apt-get install -y git \
    libaprutil1-dev \
    libapr1-dev \
    libpng12-dev \
    libjpeg62-dev \
    libcurl4-gnutls-dev \
    libpcre3-dev \
    libpixman-1-dev \
    libgdal1-dev \
    libgeos-dev \
    libsqlite3-dev \
    libdb-dev \
    libtiff4-dev

# Install Mapcache itself
RUN git clone https://github.com/mapserver/mapcache/ /usr/local/src/mapcache
RUN mkdir /usr/local/src/mapcache/build && \
    cd /usr/local/src/mapcache/build && \
    cmake ../ -DWITH_FCGI=0 -DWITH_APACHE=0 -DWITH_PCRE=1 -DWITH_TIFF=1 -DWITH_BERKELEY_DB=1 -DWITH_MEMCACHE=1 && \
    make && \
    make install

# Install Node Mapcache. This installs to `/node_modules` so will always be found
RUN git clone https://github.com/geo-data/node-mapcache/ /usr/local/src/node-mapcache
RUN npm config set mapcache:build_dir /usr/local/src/mapcache/build && \
    npm install /usr/local/src/node-mapcache

# Run the Node Mapcache tests by default
CMD npm test mapcache
