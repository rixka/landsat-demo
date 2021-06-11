# Landsat Demo
A modular Landsat image collection system with event driven image analysis.

### Requirement Specification:
* Docker
* Python and pip

### Instructions:
1. Create an s3 bucket to store code artifacts in.
2. Review the Cloudformation script `./cloudformation.yaml` and make any modifications to the parameters i.e S3 code bucket name and `UniqSuffix`.
3. Review the makefile `Makefile` and be sure to overwrite the `CODE_BUCKET` variable.
4. Pull the submodule for `./layers/aws-cli`  with the following command `git submodule update --init --recursive`. 
5. Run the command `make whole-enchilada CODE_BUCKET=${YOUR_NEW_CODE_BUCKET}` to build, upload, and deploy the demo.

**Additional:**
This deployment does not include an Event Rule to trigger the State Machine or any subscriptions to the SNS topic. If you would like to configure these or any other amendments feel free to modify the cloudformation script or create via the console.

**INFO:**
The `make whole-enchilada` command will do the following:

1. Clear and remove any build directories for a fresh build and deployment.
2. Package up the lambda functions and lambda layers. Note: one of the lambda layers is built uding Docker to avoid import errors.
3. Copy all build arttifacts to the S3 bucket `${CODE_BUCKET}`. Note: Make sure you overwrite the default values.
4. Deploys the cloudformation script which will create: S3 bucket, DynamoDB Table, Several lambda functions and lambda layers, State Machine, SNS Topic, and relevent IAM Roles.

_For more informaiton run_ `make help` _or review the makefile. You can also review the bash scripts that package the lambda layers in_ `./layers/**/`
