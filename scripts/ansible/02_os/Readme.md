## Objective
This module is to setup the target operating system environment.

## NOTE
Read the readme.md of user.admin for the assumptions.

## Structure
.
├── Readme.md
├── plays
│   ├── roles
│   │   ├── docker       <---- Setup docker group/users (beware the risk), not install package here.
│   │   ├── ntp          <---- NTP setup
│   │   └── swapoff      <---- Disable swap
│   └── site.yml
└── scripts
    └── main.sh          <---- Execution script for the module
