#!/usr/bin/env python3

from aws_cdk import core

from api_gateway_examples.api_gateway_examples_stack import ApiGatewayExamplesStack


app = core.App()
ApiGatewayExamplesStack(app, "api-gateway-examples")

app.synth()
