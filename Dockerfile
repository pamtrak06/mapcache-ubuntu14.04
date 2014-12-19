FROM pamtrak06/ubuntu14.04-apache2

MAINTAINER pamtrak06 <pamtrak06@gmail.com>

# Install mapcache compilation prerequisites
RUN apt-get install -y software-properties-common g++ make cmake

# Install mapcache dependencies provided by Ubuntu repositories
RUN apt-get install -y \
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

# Compile Mapcache for Apache
RUN mkdir /usr/local/src/mapcache/build && \
    cd /usr/local/src/mapcache/build && \
    cmake ../ -DWITH_FCGI=0 -DWITH_APACHE=1 -DWITH_PCRE=1 -DWITH_TIFF=1 -DWITH_BERKELEY_DB=1 -DWITH_MEMCACHE=1 -DCMAKE_PREFIX_PATH="/etc/apache2" && \
    make && \
    make install

# Apache configuration for mapcache
RUN echo "LoadModule mapcache_module    /usr/lib/apache2/modules/mod_mapcache.so" > /etc/apache2/mods-available/mapcache.load
RUN echo "<IfModule mapcache_module>" > /etc/apache2/mods-available/mapcache.conf
RUN echo "   <Directory /etc/apache2/conf-available>" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "      Require all granted" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "   </Directory>" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "   MapCacheAlias /mapcache \"/etc/apache2/conf-available/mapcache.xml\"" >> /etc/apache2/mods-available/mapcache.conf
RUN echo "</IfModule>" >> /etc/apache2/mods-available/mapcache.conf

# Enable mapcache module in Apache
RUN a2enmod mapcache

# Force buit libraries dependencies
RUN ldconfig

# Install OGC library
RUN pip install OWSLib
# Set path for mapcache file
RUN cd /etc/apache2/conf-available/
# Download py library to produce mapcache.xml from a wms url
RUN curl -O https://raw.githubusercontent.com/pamtrak06/mapcache/master/mapcache.py
# Build mapcache.xml sample
RUN python mapcache.py --wms http://geo.weather.gc.ca/geomet/?lang=E --prj mapcache

# Create temp directory for mapcache tiles
RUN mkdir /tmp/mapcache
RUN chmod 777 /tmp/mapcache

# Volumes
VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]

# Expose ports
EXPOSE 22 80 443

# Define default command
CMD ["apachectl", "-D", "FOREGROUND"]
