"""Example PySpark Script.

    AWS current versions for Glue 2.0
    ==============

        - Python 3.6
        - Spark 2.4

    Steps
    ======

        1. Start Glue Context
        2. Initialize Job
        3. Clear bucket contents
        4. Load dynamic dataframe for each database table
        5. Process Dynamo database
"""
import logging
import re
import sys

import boto3
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

logger = logging.getLogger(__name__)


def console(text):
    """Return data for Cloudwatch logs."""
    line = "*" * (len(text) + 3)
    formatted_text = "\n{}\n{}...\n{}\n".format(line, text, line)
    logger.warning("\033[93m{}\033[0m".format(formatted_text))


def get_args():
    """Get args from command line"""
    args = getResolvedOptions(
        sys.argv, ["JOB_NAME", "athena_database", "target_bucket"]
    )
    console("Using Arguments: {}".format(args))
    return args


def main():
    console("Starting Job")

    ## @params: [job_name]
    # 1. Start Glue Context
    glueContext = GlueContext(SparkContext.getOrCreate())

    # 2. Initialize Job
    job = Job(glueContext)
    args = get_args()
    job.init(args["JOB_NAME"], args)

    client = boto3.client("glue", region_name="us-east-1")

    Tables = client.get_tables(DatabaseName=args["athena_database"])
    tableList = Tables["TableList"]

    # 3. Clear bucket contents
    console(f"Excluding S3 files for: {args['target_bucket']}")
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(args["target_bucket"])
    bucket.objects.delete()

    for table in tableList:
        tableName = table["Name"]
        if re.search(f"[0-9]+", tableName):
            # Ignoring Athena Tables already processed...
            continue
        else:
            console("Processing Table {}".format(tableName))

        # 4. Load dynamic dataframe
        datasource0 = glueContext.create_dynamic_frame.from_catalog(
            database=args["athena_database"],
            table_name=tableName,
            transformation_ctx="datasource0",
        )
        # 5. Process Dynamo database
        # Drop null fields
        dropnullfields1 = DropNullFields.apply(
            frame=datasource0, transformation_ctx="dropnullfields1"
        )

        # Save Dynamic Frame on S3 using Glue
        glueContext.write_dynamic_frame.from_options(
            frame=dropnullfields1,
            connection_type="s3",
            connection_options={
                "path": "s3://{}/{}/".format(args["target_bucket"], tableName)
            },
            format="parquet",
            transformation_ctx="datasink2",
        )
    job.commit()


if __name__ == "__main__":
    main()
