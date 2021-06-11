#!/bin/bash

# Temporary directory for the virtual environment
export VIRTUAL_ENV_DIR="numpy-pillow-virtualenv"

# Temporary directory for AWS CLI and its dependencies
export LAMBDA_LAYER_DIR="python"

# The zip file that will contain the layer
export ZIP_FILE_NAME="numpy-pillow-lambda-layer.zip"

# Runs docker to build the packages as numpy installation in macos has an issue in lambda
docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
    pip install -r requirements.txt --no-deps -t ${LAMBDA_LAYER_DIR}

# Zips the contents of the temporary directory
zip -r ../builds/${ZIP_FILE_NAME} ${LAMBDA_LAYER_DIR}

# Removes virtual env and temp directories
rm -r ${LAMBDA_LAYER_DIR}
