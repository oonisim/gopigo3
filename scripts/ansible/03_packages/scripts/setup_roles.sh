#!/bin/bash
_DIR=$(realpath $(dirname $0))
_ROLE_DIR="${_DIR}/../plays/roles"

roles=(
    "gantsign.intellij"
    "cmprescott.chrome"
    "vmware.vmware-workstation"
    "andrewrothstein.anaconda"
)

for role in "${roles[@]}"
do
    ansible-galaxy install --roles-path ${_ROLE_DIR} ${role}
done

#--------------------------------------------------------------------------------
# R & R Server (using https://github.com/Oefenweb repositories)
# R server service starts and listesn on 8787 (login with Linux account credential).
#--------------------------------------------------------------------------------
echo "Downloading R & R Server (using https://github.com/Oefenweb repositories) ..."
mkdir -p ${_ROLE_DIR}/oefenweb_r && \
curl -L https://github.com/Oefenweb/ansible-r/tarball/master |\
tar -xz --overwrite --strip 1 -C ${_ROLE_DIR}/oefenweb_r

mkdir -p ${_ROLE_DIR}/oefenweb_rstudio_server && \
curl -L https://github.com/Oefenweb/ansible-rstudio-server/tarball/master |\
tar -xz --overwrite --strip 1 -C ${_ROLE_DIR}/oefenweb_rstudio_server
