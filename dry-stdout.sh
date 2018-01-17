mkdir -p /opt/instantclient_12_2
unzip -d /opt/instantclient_12_2 /mnt/vmex/oracle-instant-client-12/instantclient-basic-linux.x64-12.2.0.1.0.zip
unzip -d /opt/instantclient_12_2 /mnt/vmex/oracle-instant-client-12/instantclient-jdbc-linux.x64-12.2.0.1.0.zip
unzip -d /opt/instantclient_12_2 /mnt/vmex/oracle-instant-client-12/instantclient-precomp-linux.x64-12.2.0.1.0.zip
unzip -d /opt/instantclient_12_2 /mnt/vmex/oracle-instant-client-12/instantclient-sdk-linux.x64-12.2.0.1.0.zip
unzip -d /opt/instantclient_12_2 /mnt/vmex/oracle-instant-client-12/instantclient-sqlplus-linux.x64-12.2.0.1.0.zip
unzip -d /opt/instantclient_12_2 /mnt/vmex/oracle-instant-client-12/instantclient-tools-linux.x64-12.2.0.1.0.zip
find /opt/instantclient_12_2/instantclient_12_2 -mindepth 1 -maxdepth 1 -exec mv -t /opt/instantclient_12_2 {} +
rmdir /opt/instantclient_12_2/instantclient_12_2
chmod u+w /opt/instantclient_12_2/sqlplus
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/sqlplus
chmod u+w /opt/instantclient_12_2/sdk/proc
patchelf --set-rpath '$ORIGIN/..' /opt/instantclient_12_2/sdk/proc
chmod u+w /opt/instantclient_12_2/libclntshcore.so.12.1
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libclntshcore.so.12.1
chmod u+w /opt/instantclient_12_2/libclntsh.so.12.1
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libclntsh.so.12.1
chmod u+w /opt/instantclient_12_2/libipc1.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libipc1.so
chmod u+w /opt/instantclient_12_2/libmql1.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libmql1.so
chmod u+w /opt/instantclient_12_2/libnnz12.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libnnz12.so
chmod u+w /opt/instantclient_12_2/libocci.so.12.1
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libocci.so.12.1
chmod u+w /opt/instantclient_12_2/libociei.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libociei.so
chmod u+w /opt/instantclient_12_2/libocijdbc12.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libocijdbc12.so
chmod u+w /opt/instantclient_12_2/libons.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libons.so
chmod u+w /opt/instantclient_12_2/liboramysql12.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/liboramysql12.so
chmod u+w /opt/instantclient_12_2/libheteroxa12.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libheteroxa12.so
chmod u+w /opt/instantclient_12_2/libsqlplusic.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libsqlplusic.so
chmod u+w /opt/instantclient_12_2/libsqlplus.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libsqlplus.so
chmod u+w /opt/instantclient_12_2/libnfsodm12.so
patchelf --set-rpath '$ORIGIN' /opt/instantclient_12_2/libnfsodm12.so
mkdir /opt/instantclient_12_2/lib
ln -s ../libclntshcore.so.12.1 /opt/instantclient_12_2/lib/libclntshcore.so.12.1
ln -s ../libclntsh.so.12.1 /opt/instantclient_12_2/lib/libclntsh.so.12.1
ln -s ../libipc1.so /opt/instantclient_12_2/lib/libipc1.so
ln -s ../libmql1.so /opt/instantclient_12_2/lib/libmql1.so
ln -s ../libnnz12.so /opt/instantclient_12_2/lib/libnnz12.so
ln -s ../libocci.so.12.1 /opt/instantclient_12_2/lib/libocci.so.12.1
ln -s ../libociei.so /opt/instantclient_12_2/lib/libociei.so
ln -s ../libocijdbc12.so /opt/instantclient_12_2/lib/libocijdbc12.so
ln -s ../libons.so /opt/instantclient_12_2/lib/libons.so
ln -s ../liboramysql12.so /opt/instantclient_12_2/lib/liboramysql12.so
ln -s ../libheteroxa12.so /opt/instantclient_12_2/lib/libheteroxa12.so
ln -s ../libsqlplusic.so /opt/instantclient_12_2/lib/libsqlplusic.so
ln -s ../libsqlplus.so /opt/instantclient_12_2/lib/libsqlplus.so
ln -s ../libnfsodm12.so /opt/instantclient_12_2/lib/libnfsodm12.so
ln -s libclntsh.so.12.1 /opt/instantclient_12_2/lib/libclntsh.so
ln -s libclntsh.so.12.1 /opt/instantclient_12_2/libclntsh.so
mkdir /opt/instantclient_12_2/bin
ln -s ../sqlplus /opt/instantclient_12_2/bin/sqlplus
ln -s ../sdk/proc /opt/instantclient_12_2/bin/proc
ln -s ../sdk/include /opt/instantclient_12_2/precomp/public
cp /opt/instantclient_12_2/precomp/admin/pcscfg.cfg /opt/instantclient_12_2/precomp/admin/pcscfg.cfg.bak
sed -i 's@^sys_include=.*$@sys_include=($ORACLE_HOME/sdk/include,/usr/include,/usr/lib/gcc/x86_64-redhat-linux/7/include,/usr/include/linux)@' /opt/instantclient_12_2/precomp/admin/pcscfg.cfg
mkdir -p /opt/instantclient_12_2/network/admin
cp work/tnsnames.ora /opt/instantclient_12_2/network/admin/tnsnames.ora
echo 'add this to your profile: export ORACLE_HOME=/opt/instantclient_12_2; export PATH=$ORACLE_HOME/bin:$PATH'
