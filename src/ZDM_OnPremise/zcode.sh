#!/bin/sh
domain="${1:-onprem.example.com}"
export ZERYNTH_ZDM_URL="https://api.zdm.${domain}/v3"
export ZERYNTH_LOGIN_URL="http://login.${domain}/login"
zcode .
