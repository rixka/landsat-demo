import csv
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

filename = 'L8_path_row.csv'


def lambda_handler(event, context):
    return {
        'detail': {
            'prefixes': gen_prefixes(filename)
        }
    }


def gen_prefixes(filename):
    prefixes = []

    logger.info("Reading file: \"{}\"".format(filename))
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Generate something like: c1/L8/200/019/LC08_L1GT_200019_2021...
            prefixes.append({
                "prefix": "c1/L8/{}/{}/LC08_L1GT_200019_".format(
                    row['Path'], row['Row']
                )
            })

    logger.info("Generated prefixes from file:\n---\n{}\n---".format(prefixes))
    return prefixes
