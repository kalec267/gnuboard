#!/bin/sh
set -eu

# Windows 명령행을 통과하는 중첩 인용부호 없이 컨테이너 안에서 자격 증명을 사용한다.
export MYSQL_PWD="${MARIADB_PASSWORD:?MARIADB_PASSWORD is required}"
case "${1:-probe}" in
    probe)
        exec mariadb --user="$MARIADB_USER" --database="$MARIADB_DATABASE" \
            --batch --skip-column-names --execute="SHOW TABLES LIKE 'g5_config'"
        ;;
    backup)
        exec mariadb-dump --lock-tables --user="$MARIADB_USER" "$MARIADB_DATABASE"
        ;;
    restore)
        exec mariadb --user="$MARIADB_USER" "$MARIADB_DATABASE"
        ;;
    *)
        echo 'Unknown database operation. Use probe, backup or restore.' >&2
        exit 2
        ;;
esac
