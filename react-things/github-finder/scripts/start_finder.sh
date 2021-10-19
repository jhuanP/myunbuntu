#!/usr/bin/bash
. ~/.nvm/nvm.sh && \
cd /var/lib/jenkins/react-things && \
npm install && \
nohup npm start > /dev/null 2> /dev/null < /dev/null &
