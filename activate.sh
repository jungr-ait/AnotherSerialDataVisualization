#! /bin/bash
################################################################################
#
# Copyright (C) 2023 Roland Jung, University of Klagenfurt, Austria.
#
# All rights reserved.
#
# This software is licensed under the terms of the MIT License, the full terms 
# of which are made available in the LICENSE file.
#
# You can contact the author at roland.jung@aau.at
#
################################################################################
echo "activate the python environment..."
CUR_DIR=${PWD}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV_DIR=${DIR}/python-venv


#bash update_submodules.sh

# create virtual environment
if [ ! -d "$VENV_DIR" ]; then
  source setup-env.sh   
fi  

source ${VENV_DIR}/env/bin/activate
which python3
