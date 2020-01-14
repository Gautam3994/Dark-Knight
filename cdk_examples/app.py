#!/usr/bin/env python3

from aws_cdk import core, aws_iam

from cdk_examples.cdk_examples_stack import CdkExamplesStack


app = core.App()
CdkExamplesStack(app, "cdk-examples", env={'region': 'us-east-2'})

app.synth()
