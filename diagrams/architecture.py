#!/usr/bin/env python3

from diagrams import Diagram
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.aws.compute import Fargate
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import ECR

from diagrams.generic.device import Mobile

from diagrams.custom import Custom

with Diagram('Travel Data Pipeline', show=False):
    mobile = Mobile('IOS Shortcuts')
    s3_proxy = APIGateway('S3 Proxy')
    s3 = S3('Pipeline Bucket')
    event_bridge = Eventbridge('Event Router')
    fargate = Fargate('Fargate')
    dynamodb = Dynamodb('DynamoDB')
    ddb_proxy = APIGateway('DynamoDB Proxy')

    github = Custom('Github Repo', './resources/github.png')
    gh_actions = Custom('Github Actions', './resources/github_actions.png')
    ecr = ECR('Container Registry')
    github >> gh_actions >> ecr >> fargate

    mobile >> s3_proxy >> s3 >> event_bridge >> fargate >> dynamodb >> ddb_proxy
