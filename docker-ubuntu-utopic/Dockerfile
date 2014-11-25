# Model from https://github.com/geo-data/node-mapcache
#
# This creates an Ubuntu derived base image that installs a recent
# version of Node.js as well as the latest repository checkouts of
# Mapserver Mapcache and the Node Mapcache bindings.  Mapcache has a
# broad range of compile time options enabled and as such this
# provides a suitable base image for both experimenting with and
# deriving production ready images from.
#

FROM ubuntu:utopic

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
# libjpeg62-dev dependencies
RUN apt-get install -y libc-dev
# libpcre3-dev dependencies
RUN apt-get install -y libc6-dev \
    libpcre3
#libpng12-dev dependencies
RUN apt-get install -y libpng12-0 \
    zlib1g-dev
# libsqlite3-dev dependencies
RUN apt-get install -y libsqlite3-0 \
    libc6-dev
# libtiff4-dev dependencies
RUN apt-get install -y libc6-dev \
    libc-dev \
    zlib1g-dev
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
