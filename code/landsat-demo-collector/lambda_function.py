import logging
import subprocess

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    filename = event['key'].split("/")[-1]
    cmd_download = '/opt/aws s3 cp ' + event['key'] + ' /tmp/data/ --no-sign-request'
    cmd_upload = '/opt/aws s3 cp /tmp/data/' + filename + ' ' + event['bucket']
    run_command(cmd_download)
    run_command(cmd_upload)
    return


def run_command(command):
    command_list = command.split(' ')

    try:
        logger.info("Running shell command: \"{}\"".format(command))
        result = subprocess.run(command_list, stdout=subprocess.PIPE);
        logger.info("Command output:\n---\n{}\n---".format(result.stdout.decode('UTF-8')))
    except Exception as e:
        logger.error("Exception: {}".format(e))
        return False

