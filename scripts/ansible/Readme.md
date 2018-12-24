# Objective
Setup GoPiGo3 Raspbery for Robots


## Directory Structure
Configurations are broken down into modules (e.g. prerequisites, os, packages, etc)

```
HOME
├───ansible
│   └───linux_soe            <----- SCRIPT_DIR
│       ├───01_prerequisite       <----- Module to setup Ansible pre-requisites (Ansible master and target)
│       │   ├───plays             <----- Ansible playbook directory
│       │   │   └───roles         <----- Ansible role directory
│       │   └───scripts           <----- Script to execute Ansible playbooks
│       ├───02_os
│       │   ├───plays
│       │   │   └───roles
│       │   └───scripts
│       └───03_packages
│           ├───plays
│           │   └───roles
│           └───scripts
├───conf                          <----- Configurations are isolated in the directory only (separate configurations from codes)
│   └───ansible                   <----- CONF_DIR : Ansible configurations
│       └───inventories           <----- Parent directory of target environment on which Ansible runs playbooks against.
│           └───robot001
│               ├───group_vars
│               │   └───all       <----- Ansible group variables
│               └───inventory     <----- Information on the target servers in the inventory
└───tools                         <----- TOOL_DIR
```

## Module and structure

Module is a set of playbooks and roles to execute a specific task e.g. 03_packages is to install packages with the package manager of the disribution (apt for Ubuntu). Each module directory has the same structure having Readme, Plays, and Scripts.
```
├── 03_packages
│   ├── plays
│   │   ├── roles
│   │   │   ├── site.common        <----- Common packages e.g. zip, wget, zip, etc.
│   │   │   ├── site.java          <----- Each role fulfill one specific responsibility (package)
│   │   │   ├── site.postman
│   │   │   └── gantsign.intellij
│   │   └── site.yml               <------ Main Ansible playbook of the module
│   ├── Readme.md
│   └── scripts
│       ├── main.sh                <------ Main bash script to run the module
│       ├── _posttask.sh
│       ├── _pretask.sh
│       └── _utility.sh
```
---

# Preparations
## MacOS
To be able to user [realpath](https://stackoverflow.com/questions/3572030/bash-script-absolute-path-with-osx).
```
brew install coreutils
```

## Ansible master
Ansible master is the host in which the Ansible playbooks (scripts) are executed.

#### SSH keys
Generate SSH key pair or import existing. The public key needs to be copied to the target machine for SSH public key login without password-less login.

#### Ansible runtime and pre-requisites
If the host is RHEL/CentOS/Ubuntu, run below will setup the pre-requisites to run Ansible in the Ansible master machine.

```
(cd SCRIPT_DIR/01_prerequisite/scripts && ./setup.sh)
```



## Ansible target

#### SSHD
SSH server is not installed/enabled by default in some distributions e.g. Ubuntu.

#### REMOTE_USER
Set the default Linux account that can sudo without password as the Ansible remote_user to run the playbooks If using another account, configure it and make sure it can sudo without password and configure .ssh/config.

```
(cd SCRIPT_DIR/01_prerequisite/scripts && ./setup_remote_user.sh)

```

---
# Configurations

## Parameters

Parameters for an environment are all isolated in group_vars of the environment inventory. Go through the group_vars files to set values.

```
.
├── conf
│   └── ansible
│      ├── ansible.cfg
│      └── inventories
│           └── linux_soe
│               ├── group_vars
│               │   ├── all             <---- Configure properties in the 'all' group vars
│               │   │   ├── server.yml  <---- Server parameters e.g. location of kubelet configuration file
│               │   │   └── env.yaml
│               └── inventory
│                   └── hosts           <---- Target node(s) using tag values (set upon creating AWS env)
```


---

# Execution

## SSH agent
Configure ssh-agent and/or .ssh/config with the AWS SSH PEM to be able to SSH into the targets without providing pass phrase.

```
eval $(ssh-agent)
ssh-add <AWS SSH pem>
ssh ${REMOTE_USER}@<server> sudo ls  # no prompt for asking password

```

## Run Ansible playbooks
Run HOME/run_ansible_linux.sh to run all at once or go through the configurations and executions step by step below.
Alternatively, run each module one by one, and skip 10_datadog if not using.
```
pushd ${SCRIPT_BASE}/${MODULE}/scripts && ./main.sh or
${SCRIPT_BASE}/${MODULE}/scripts/main.sh aws <ansible remote_user>
```

Module is either of:
```
├── 01_prerequisite      <---- Module to setup Ansible pre-requisites
├── 02_os                <---- Module to setup OS
├── 03_packages          <---- Module to install packages
├── conductor.sh         <---- Script to conduct playbook executions
└── player.sh            <---- Playbook player
```


---

