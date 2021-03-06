#!/bin/bash
#--------------------------------------------------------------------------------
# [Function]
# Go to the PLAYBOOK_DIR, setup Ansible inventory/cfg, invoke PALYER to play books
# against the ENVIRONMENT with REMOTE_USER.
# 1. PLAYBOOK_DIR:
# 2. ENVIRONMENT
# 3. REMOTE_USER
#--------------------------------------------------------------------------------
set -eu

if [ $# -lt 3 ] ; then
    echo "Insufficient argument"
    echo "$0 PLAYBOOK_DIR ENVIRONMENT REMOTE_USER"
    exit 1
fi

DIR=$(realpath $(dirname $0))
PLAY_DIR=$1
ENVIRONMENT=$2
REMOTE_USER=$3

shift 3
ARGS=$@

#CONF_DIR=${CONF_DIR:?'Set CONF_DIR'}
#TOOL_DIR=${TOOL_DIR:?'Set TOOL_DIR'}

. ${DIR}/_utility.sh
CONF_DIR=$(_locate ${DIR} '/' 'conf/ansible')
TOOL_DIR=$(_locate ${DIR} '/' 'tools')

PLAYER=${DIR}/player.sh

#--------------------------------------------------------------------------------
# Go to the playbook directory.
#--------------------------------------------------------------------------------
cd ${PLAY_DIR}

#--------------------------------------------------------------------------------
# Setup the play ground for Ansible player.
#--------------------------------------------------------------------------------
rm -rf \
    ${PLAY_DIR}/{callbacks,group_vars,ansible.cfg,hosts}

cp -r  ${CONF_DIR}/inventories/${ENVIRONMENT}/inventory hosts
ln -sf ${CONF_DIR}/inventories/${ENVIRONMENT}/group_vars
ln -sf ${CONF_DIR}/ansible.cfg
ln -sf ${CONF_DIR}/callbacks



#--------------------------------------------------------------------------------
# Let the player play the books.
#--------------------------------------------------------------------------------
#VAULT_PASS_FILE=${CONF_DIR}/ansible/vaultpass.encrypted
#VAULT_PASS=$(${TOOL_DIR}/decrypt.sh ${DECRYPT_KEY_FILE} ${VAULT_PASS_FILE})
#${PLAYER} ${VAULT_PASS} ${REMOTE_USER} ${ARGS}

ansible-playbook -vvvvv -i hosts --limit "environment" --user ${REMOTE_USER} ${ARGS} site.yml --vault-password-file ~/.ansible/.vault_pass.txt
#ansible-playbook -vvvv -i hosts --limit "environment" --user ${REMOTE_USER} ${ARGS} site.yml

#--------------------------------------------------------------------------------
# Clean up
#--------------------------------------------------------------------------------
set -x
rm -rf \
    ${PLAY_DIR}/{callbacks,group_vars,ansible.cfg,hosts}
