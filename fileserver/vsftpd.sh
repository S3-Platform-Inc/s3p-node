#!/bin/bash

set -e
source /etc/container_environment.sh


[ -f /etc/vsftpd.conf ] || cat <<EOF > /etc/vsftpd.conf


write_enable=YES
upload_enable=YES
force_dot_files=YES
mkdir_write_enable=YES
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
chown_uploads=YES
chown_username=adminuser
delete_failed_uploads=yes
anon_umask=0000
chown_upload_mode=0777
file_open_mode=0777
EOF

exec /usr/sbin/vsftpd