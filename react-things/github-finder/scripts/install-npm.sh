#!/usr/bin/bash

sudo yum update -y && \
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash && \
. ~/.nvm/nvm.sh && \
nvm install  && \
nvm install node && \
nvm install 10.19 && \
nvm use 10.19
 
