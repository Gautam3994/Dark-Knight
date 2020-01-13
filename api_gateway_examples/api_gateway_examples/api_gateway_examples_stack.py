from aws_cdk import core, aws_lambda, aws_apigateway
from aws_cdk.aws_iam import Role, ServicePrincipal, Policy, PolicyStatement, Effect


class ApiGatewayExamplesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        lambda_role_for_cloudwatch = Role(self, id="RoleToCreateLogs",
                                          assumed_by=ServicePrincipal("lambda.amazonaws.com"),
                                          role_name="RoleToCreateLogs")
        Policy(self, id="log_creation_policy_for_lambda",
               policy_name="log_creation_policy_for_lambda",
               statements=[PolicyStatement(effect=Effect.ALLOW,
                                           actions=["logs:CreateLogGroup",
                                                    "logs:CreateLogStream",
                                                    "logs:PutLogEvents"],
                                           resources=["arn:aws:logs:*:*:*"])
                           ], roles=[lambda_role_for_cloudwatch])
        faker_layer = aws_lambda.LayerVersion(self, "Layer_for_faker_module",
                                              code=aws_lambda.Code.from_asset(
                                                  "/home/darkknight/PycharmProjects/Layers/faker"),
                                              compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_6],
                                              license="Apache-2.0",
                                              description="A layer to add the faker module to lambda"
                                              )
        lambda_get_inventory_function = aws_lambda.Function(self, "lambda_get_inventory_function",
                                                            function_name="lambda_get_inventory_function",
                                                            code=aws_lambda.Code.from_asset(
                                                                "/home/darkknight/PycharmProjects/lambda_functions/getinventory"),
                                                            handler="getinventory.handler",
                                                            runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                            description="function to get and post values on api calls",
                                                            role=lambda_role_for_cloudwatch, layers=[faker_layer])
        api_gateway_backend_inventory = aws_apigateway.RestApi(self, "api_gateway_for_inventory",
                                                               rest_api_name="api for inventory management_new",
                                                               description="api gateway to access the inventory table",
                                                               cloud_watch_role=True,
                                                               endpoint_types=[aws_apigateway.EndpointType.REGIONAL])
        shoes_resource = api_gateway_backend_inventory.root.add_resource("shoes")
        emptymodel = aws_apigateway.Model.EMPTY_MODEL
        shoe_get_method = shoes_resource.add_method(http_method="GET",
                                                    integration=aws_apigateway.LambdaIntegration(
                                                        handler=lambda_get_inventory_function,
                                                        proxy=False,
                                                        integration_responses=[aws_apigateway.IntegrationResponse(
                                                            status_code='200',
                                                            response_parameters={
                                                                "method.response.header.Access-Control-Allow-Headers": "'Content-Type, X-Amz-Date, Authorization'",
                                                                "method.response.header.Access-Control-Allow-Methods": "'GET, PUT'",
                                                                "method.response.header.Access-Control-Allow-Origin": "'*'"
                                                            }
                                                        )]

                                                    ),
                                                    method_responses=[aws_apigateway.MethodResponse(status_code='200',
                                                                                                    response_parameters={
                                                                                                        "method.response.header.Access-Control-Allow-Headers": True,
                                                                                                        "method.response.header.Access-Control-Allow-Methods": True,
                                                                                                        "method.response.header.Access-Control-Allow-Origin": True
                                                                                                    },
                                                                                                    response_models={
                                                                                                        "application/json": emptymodel
                                                                                                    }
                                                                                                    )])
        lambda_get_order_status_function = aws_lambda.Function(self, "lambda_get_order_status_function",
                                                               function_name="lambda_get_order_status_function",
                                                               code=aws_lambda.Code.from_asset(
                                                                   "/home/darkknight/PycharmProjects/lambda_functions/getorder"),
                                                               handler="getorder.handler",
                                                               runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                               description="function to get order status on api calls",
                                                               role=lambda_role_for_cloudwatch, layers=[faker_layer])
        order_resource = api_gateway_backend_inventory.root.add_resource("order")
        order_post_method = order_resource.add_method(http_method="POST", integration=aws_apigateway.LambdaIntegration(handler=lambda_get_order_status_function,
                                                                                                                       proxy=True))
        order_resource_get = order_resource.add_resource("{id}")
        order_post_method = order_resource_get.add_method(http_method="GET", integration=aws_apigateway.LambdaIntegration(
            handler=lambda_get_order_status_function,
            proxy=False,
            integration_responses=[aws_apigateway.IntegrationResponse(
                status_code='200',
                response_parameters={
                    "method.response.header.Access-Control-Allow-Headers": "'Content-Type, X-Amz-Date, Authorization'",
                    "method.response.header.Access-Control-Allow-Methods": "'GET, PUT'",
                    "method.response.header.Access-Control-Allow-Origin": "'*'"
                }
            )]

        ), method_responses=[
                                                              aws_apigateway.MethodResponse(status_code='200',
                                                                                            response_parameters={
                                                                                                "method.response.header.Access-Control-Allow-Headers": True,
                                                                                                "method.response.header.Access-Control-Allow-Methods": True,
                                                                                                "method.response.header.Access-Control-Allow-Origin": True
                                                                                            },
                                                                                            response_models={
                                                                                                "application/json": emptymodel
                                                                                            }
                                                                                            )])
