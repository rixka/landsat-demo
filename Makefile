#
# Makefile for landsat-demo-project
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

MAKE := $(MAKE) --no-print-directory

STACK_NAME ?= landsat-demo
REGION ?= eu-west-2
CODE_BUCKET ?= "$(STACK_NAME)-code"

.PHONY: help clean whole-enchilada package s3-upload deploy
.DEFAULT_GOAL : help

help:
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make package           packages lambda functions'
	@echo '    make s3-upload         uploads hard coded objects to s3'
	@echo '    make deploy            deploys cloudformation script'
	@echo '    make clean             removes old build directories ./builds and ./layers/builds'
	@echo '    make whole-enchiliada  packages, uploads, and deploys stack'
	@echo

package:
	@echo
	@echo 'Packaging lambda functions to ./builds'
	@echo
	mkdir -p ./builds
	find ./code/* -type d -exec zip -rj {}.zip {} -x *.DS_Store \; -exec mv {}.zip ./builds/ \;
	@echo
	@echo 'Packaging lambda layers to ./layers/builds'
	@echo
	mkdir -p ./layers/builds
	cd ./layers/aws-cli && ./awscli-lambda-package_macos.sh
	# I could change the script to make the zip in ./layers/builds but I want
	# to maintain credit and integrity to the author ilyabezdelev
	mv ./layers/aws-cli/awscli-lambda-layer.zip ./layers/builds/
	cd ./layers/numpy-pillow && ./get_layer_packages.sh

whole-enchilada: clean package s3-upload deploy

clean:
	@echo
	@echo 'Removing old builds'
	@echo
	rm -r builds ./layers/builds/

s3-upload:
	@echo
	@echo 'Uploading zip files to s3://$(CODE_BUCKET)'
	@echo
	aws s3 cp ./builds/ s3://$(CODE_BUCKET) --recursive --exclude '*' --include '*.zip'
	aws s3 cp ./layers/builds/ s3://$(CODE_BUCKET)/layers --recursive --exclude '*' --include '*.zip'

deploy:
	@echo
	@echo 'Deploying $(STACKNAME) in region $(REGION)'
	@echo
	aws cloudformation deploy --template-file cloudformation.yaml \
	--stack-name $(STACK_NAME) --region $(REGION) \
	--parameter-overrides CodeBucket=$(CODE_BUCKET) \
	--capabilities CAPABILITY_NAMED_IAM
