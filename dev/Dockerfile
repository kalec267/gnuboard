FROM php:8.3-apache-bookworm
RUN apt-get update && apt-get install -y --no-install-recommends libpng-dev libjpeg62-turbo-dev libfreetype6-dev libonig-dev libcurl4-openssl-dev libxml2-dev \
 && docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install -j2 mysqli gd mbstring curl soap \
 && rm -rf /var/lib/apt/lists/* \
 && usermod -u 1000 www-data && groupmod -g 1000 www-data \
 && sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf \
 && sed -i 's/:80>/:8080>/' /etc/apache2/sites-available/000-default.conf
COPY dev/apache.conf /etc/apache2/conf-enabled/yourday.conf
COPY dev/php.ini /usr/local/etc/php/conf.d/yourday.ini
COPY --chmod=755 dev/start-web.sh /usr/local/bin/yourday-start
WORKDIR /var/www/html
ENTRYPOINT ["/usr/local/bin/yourday-start"]
CMD ["apache2-foreground"]
