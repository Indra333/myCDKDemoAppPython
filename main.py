#!/usr/bin/env python3
import os
from pipeline.pipeline_stack import PipelineStack
import aws_cdk as cdk

app = cdk.App()

PipelineStack(app, "PipelineStack",
              env=cdk.Environment(account="390844746867", region="us-east-1")
              )

app.synth()
