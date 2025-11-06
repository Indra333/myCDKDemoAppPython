from constructs import Construct
import aws_cdk as cdk
from aws_cdk import Stack, pipelines
from app.app_stack import AppStack

GITHIB_OWNER = "Indra333"
GITHUB_REPO = "myCDKDemoAppPython"
GITHUB_BRANCH = "main"
CONNECTION_ARN = "arn:aws:codeconnections:us-east-1:390844746867:connection/fcf10cdf-06f1-49a0-8953-4e1ed84a8363"


class AppStage(cdk.Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope,id, **kwargs)
        AppStack(self, "AppStack")


class PipelineStack(Stack):
    def __init__ (self, scope:Construct, id:str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        source = pipelines.CodePipelineSource.connection(
            repo_string=f"{GITHIB_OWNER}/{GITHUB_REPO}",
            branch=GITHUB_BRANCH,
            connection_arn=CONNECTION_ARN
        )

        pipeline = pipelines.CodePipeline(
            self, "CdkPipeline",
            pipeline_name = "MyCdkPythonPipeline",
            synth= pipelines.ShellStep(
                "Synth",
                input=source,
                commands=[
                    "python -m venv .venv",
                    ". .venv/bin/activate || true",
                    "pip install -r requirements.txt",
                    "npm i -g aws-cdk",
                    "cdk synth"
                ],
                primary_output_directory="cdk.out"
            ),
            cross_account_keys=False,
        )

        pipeline.add_stage(
            AppStage(self, "Dev",
                     env =cdk.Environment(account="390844746867", region="us-east-1")
                     ))