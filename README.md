## Welcome to Glue ETL Example

[![Release](https://github.com/chrismaille/glue-demo/workflows/release/badge.svg)](https://github.com/chrismaille/glue-demo/actions)
[![Python](https://img.shields.io/badge/python-3.7-green)](https://www.python.org)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


This is ETL Example using AWS Glue Crawlers and a minimal PySpark script
to process a demo DynamoDB table

### Requirements

* [Make](https://www.gnu.org/software/make/)
* [Python3.8](https://www.python.org)
* [AWS CLI](https://aws.amazon.com/cli/)
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Poetry](https://python-poetry.org/)

### Resources Created

| Name                         | Type                  | Description                                      |
|:-----------------------------|:----------------------|:-------------------------------------------------|
| DynamoDBExample              | DynamoDb Table        | DynamoDb Table for example                       |
| GlueMicroservicesCatalog     | Glue Database         | Convert Databases schemas to Glue Catalog        |
| GlueMicroservicesDatabase    | Glue Database         | Convert S3 data to Athena Tables                 |
| MicroservicesParketBucket    | S3 Bucket             | Store Parket files                               |
| Dynamo2CatalogCrawler        | Glue Crawler          | Convert Dynamo Databases Schemas to Glue Catalog |
| Dynamo2S3Job                 | Glue Job              | Save DynamoDB tables in S3 using Glue Catalog    |
| Bucket2AthenaCrawler         | Glue Crawler          | Convert S3 data into Athena tables               |
| Dynamo2AthenaWorkflow        | Glue Workflow         | Example Workflow                                 |
| Dynamo2AthenaManualTrigger   | Glue Workflow Trigger | Executes Dynamo2CatalogCrawler                   |
| Dynamo2AthenaJobTrigger      | Glue Workflow Trigger | Executes Dynamo2S3Job                            |
| Dynamo2AthenaDatabaseTrigger | Glue Workflow Trigger | Executes Bucket2AthenaCrawler                    |
| GlueMicroservicesPolicy      | IAM Policy            | Cloudformation Needed Policies                   |

### Workflow

[![](https://mermaid.ink/img/eyJjb2RlIjoic3RhdGVEaWFncmFtLXYyXG4gICAgWypdIC0tPiBEeW5hbW8yQXRoZW5hTWFudWFsVHJpZ2dlclxuICAgIER5bmFtbzJBdGhlbmFNYW51YWxUcmlnZ2VyIC0tPiBEeW5hbW8yQ2F0YWxvZ0NyYXdsZXI6IEV4ZWN1dGVzXG4gICAgRHluYW1vMkNhdGFsb2dDcmF3bGVyIC0tPiBEeW5hbW9EQkV4YW1wbGU6IFJlYWQgU2NoZW1hXG4gICAgRHluYW1vMkNhdGFsb2dDcmF3bGVyIC0tPiBHbHVlTWljcm9zZXJ2aWNlc0NhdGFsb2c6IFNhdmUgU2NoZW1hXG4gICAgRHluYW1vMkNhdGFsb2dDcmF3bGVyIC0tPiBEeW5hbW8yQXRoZW5hSm9iVHJpZ2dlcjogT24gU3VjY2Vzc1xuICAgIER5bmFtbzJBdGhlbmFKb2JUcmlnZ2VyIC0tPiBEeW5hbW8yUzNKb2I6IEV4ZWN1dGVzXG4gICAgRHluYW1vMlMzSm9iIC0tPiBHbHVlTWljcm9zZXJ2aWNlc0NhdGFsb2c6IFJlYWQgU2NoZW1hXG4gICAgRHluYW1vMlMzSm9iIC0tPiBEeW5hbW9EQkV4YW1wbGU6IFJlYWQgYW5kIENvbnZlcnQgUmVjb3Jkc1xuICAgIER5bmFtbzJTM0pvYiAtLT4gTWljcm9zZXJ2aWNlc1BhcmtldEJ1Y2tldDogU2F2ZSBQYXJxdWV0IEZpbGVzXG4gICAgRHluYW1vMlMzSm9iIC0tPiBEeW5hbW8yQXRoZW5hRGF0YWJhc2VUcmlnZ2VyOiBPbiBTdWNjZXNzXG4gICAgRHluYW1vMkF0aGVuYURhdGFiYXNlVHJpZ2dlciAtLT4gQnVja2V0MkF0aGVuYUNyYXdsZXI6IEV4ZWN1dGVzXG4gICAgQnVja2V0MkF0aGVuYUNyYXdsZXIgLS0-IEdsdWVNaWNyb3NlcnZpY2VzRGF0YWJhc2U6IENyZWF0ZXNcbiAgICBHbHVlTWljcm9zZXJ2aWNlc0RhdGFiYXNlIC0tPiBNaWNyb3NlcnZpY2VzUGFya2V0QnVja2V0OiBMaW5rIERCIHRvIEZpbGVzXG4gICAgR2x1ZU1pY3Jvc2VydmljZXNEYXRhYmFzZSAtLT4gWypdXG4gICAgICAgICAgICAiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoic3RhdGVEaWFncmFtLXYyXG4gICAgWypdIC0tPiBEeW5hbW8yQXRoZW5hTWFudWFsVHJpZ2dlclxuICAgIER5bmFtbzJBdGhlbmFNYW51YWxUcmlnZ2VyIC0tPiBEeW5hbW8yQ2F0YWxvZ0NyYXdsZXI6IEV4ZWN1dGVzXG4gICAgRHluYW1vMkNhdGFsb2dDcmF3bGVyIC0tPiBEeW5hbW9EQkV4YW1wbGU6IFJlYWQgU2NoZW1hXG4gICAgRHluYW1vMkNhdGFsb2dDcmF3bGVyIC0tPiBHbHVlTWljcm9zZXJ2aWNlc0NhdGFsb2c6IFNhdmUgU2NoZW1hXG4gICAgRHluYW1vMkNhdGFsb2dDcmF3bGVyIC0tPiBEeW5hbW8yQXRoZW5hSm9iVHJpZ2dlcjogT24gU3VjY2Vzc1xuICAgIER5bmFtbzJBdGhlbmFKb2JUcmlnZ2VyIC0tPiBEeW5hbW8yUzNKb2I6IEV4ZWN1dGVzXG4gICAgRHluYW1vMlMzSm9iIC0tPiBHbHVlTWljcm9zZXJ2aWNlc0NhdGFsb2c6IFJlYWQgU2NoZW1hXG4gICAgRHluYW1vMlMzSm9iIC0tPiBEeW5hbW9EQkV4YW1wbGU6IFJlYWQgYW5kIENvbnZlcnQgUmVjb3Jkc1xuICAgIER5bmFtbzJTM0pvYiAtLT4gTWljcm9zZXJ2aWNlc1BhcmtldEJ1Y2tldDogU2F2ZSBQYXJxdWV0IEZpbGVzXG4gICAgRHluYW1vMlMzSm9iIC0tPiBEeW5hbW8yQXRoZW5hRGF0YWJhc2VUcmlnZ2VyOiBPbiBTdWNjZXNzXG4gICAgRHluYW1vMkF0aGVuYURhdGFiYXNlVHJpZ2dlciAtLT4gQnVja2V0MkF0aGVuYUNyYXdsZXI6IEV4ZWN1dGVzXG4gICAgQnVja2V0MkF0aGVuYUNyYXdsZXIgLS0-IEdsdWVNaWNyb3NlcnZpY2VzRGF0YWJhc2U6IENyZWF0ZXNcbiAgICBHbHVlTWljcm9zZXJ2aWNlc0RhdGFiYXNlIC0tPiBNaWNyb3NlcnZpY2VzUGFya2V0QnVja2V0OiBMaW5rIERCIHRvIEZpbGVzXG4gICAgR2x1ZU1pY3Jvc2VydmljZXNEYXRhYmFzZSAtLT4gWypdXG4gICAgICAgICAgICAiLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCJ9LCJ1cGRhdGVFZGl0b3IiOmZhbHNlfQ)

### Command List

#### Install Project

```shell
# Please install Poetry first: https://python-poetry.org/
$ make install
```

#### Deploy Demo

```shell
$ make deploy
```

#### Remove Demo

```shell
$ make remove
```
