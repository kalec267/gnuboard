#!/bin/sh
set -eu

# 외부 포트와 Apache 포트를 맞춰 그누보드의 절대 URL에도 같은 포트를 사용한다.
port="${SHOP_PORT:-8080}"
case "$port" in
    ''|*[!0-9]*) echo 'SHOP_PORT must be a number from 1024 to 65535.' >&2; exit 1 ;;
esac
if [ "${#port}" -gt 5 ] || [ "$port" -lt 1024 ] || [ "$port" -gt 65535 ]; then
    echo 'SHOP_PORT must be a number from 1024 to 65535.' >&2
    exit 1
fi
sed -i "s/^Listen [0-9][0-9]*$/Listen $port/" /etc/apache2/ports.conf
sed -i "s/<VirtualHost \*:[0-9][0-9]*>/<VirtualHost *:$port>/" /etc/apache2/sites-available/000-default.conf
exec docker-php-entrypoint "$@"
