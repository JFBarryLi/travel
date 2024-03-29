#!/usr/bin/env python3

from diagrams import Cluster, Diagram
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.aws.compute import Fargate
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import ECR
from diagrams.aws.compute import ECS
from diagrams.generic.device import Mobile
from diagrams.custom import Custom
from diagrams.saas.chat import Discord

graph_attr = {
    'fontsize': '25',
    'bgcolor': 'gray95',
}

with Diagram('Travel Data Pipeline', show=False, graph_attr=graph_attr):
    mobile = Mobile('IOS Shortcuts')
    s3_proxy = APIGateway('S3 Proxy')
    s3 = S3('Pipeline Bucket')
    event_bridge = Eventbridge('Event Router')

    with Cluster('Processing'):
        fargate = Fargate('Fargate')

        nlp = Custom('NLP', './resources/nlp.png')
        fargate >> nlp

        geocode = Custom('Geocoding', './resources/geocode.png')
        fargate >> geocode

    discord = Discord('Alerting')
    fargate >> discord

    dynamodb = Dynamodb('DynamoDB')
    ddb_proxy = APIGateway('DynamoDB Proxy')

    github = Custom('Github Repo', './resources/github.png')
    gh_actions = Custom('Github Actions', './resources/github_actions.png')
    ecr = ECR('Container Registry')
    ecs = ECS('ECS')
    gh_actions >> ecr >> fargate
    github >> gh_actions >> ecs >> fargate

    mobile >> s3_proxy >> s3 >> event_bridge >> fargate >> dynamodb >> ddb_proxy
