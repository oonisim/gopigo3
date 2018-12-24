#!/usr/bin/env bash
cd $(dirname $0)
#--------------------------------------------------------------------------------
# Set the exec permission to scripts in the repository.
#--------------------------------------------------------------------------------
find . -name '*.sh' | xargs -I % /bin/bash -c "git add %; "
find . -name '*.sh' | xargs -I % /bin/bash -c "chmod u+x %; "
find . -name '*.sh' | xargs -I % /bin/bash -c "git update-index --chmod=+x % "

#--------------------------------------------------------------------------------
# cleanup
#--------------------------------------------------------------------------------
find . -type d -name '.terraform' | xargs rm -rf
find . \( -name 'tfplan' -o -name '*.log' -o -name '*~' \) | xargs rm -f
find . -type f \( -name 'site.retry' -o -name 'ansible.log' -o -name '*~' \) | xargs rm -f
