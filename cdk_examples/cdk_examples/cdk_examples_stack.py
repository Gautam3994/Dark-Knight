from aws_cdk import core, aws_dynamodb, aws_lambda, aws_s3, aws_s3_notifications, aws_events, aws_cloudwatch, aws_kms, \
    aws_s3_deployment, aws_lambda_event_sources, aws_apigateway, aws_stepfunctions
from aws_cdk import aws_ses, aws_sns
from aws_cdk import aws_iam
from aws_cdk.aws_iam import Role, ServicePrincipal, Policy, PolicyStatement, Effect, ManagedPolicy
import os
import uuid
import aws_cdk.aws_events_targets as targets
import aws_cdk
from aws_cdk.aws_s3 import BlockPublicAccess, IBucketNotificationDestination
from aws_cdk.core import Duration


class CdkExamplesStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        dynamodb = aws_dynamodb.Table(self, "inventory table", table_name="inventory",
                                      partition_key=aws_dynamodb.Attribute(name="product_id",
                                                                           type=aws_dynamodb.AttributeType.STRING),
                                      read_capacity=1, write_capacity=1,
                                      stream=aws_dynamodb.StreamViewType.NEW_AND_OLD_IMAGES
                                      )
        lambda_role_for_s3_dynamo = Role(self, id="RoleToCreateItemsFromS3",
                                         assumed_by=ServicePrincipal("lambda.amazonaws.com"),
                                         role_name="RoleToCreateItemsFromS3")
        dynamodb_item_creation_policy_for_lambda = Policy(self, id="dynamodb_item_creation_policy_for_lambda",
                                                          policy_name="dynamodb_item_creation_policy_for_lambda",
                                                          statements=[PolicyStatement(effect=Effect.ALLOW,
                                                                                      actions=["logs:CreateLogGroup",
                                                                                               "logs:CreateLogStream",
                                                                                               "logs:PutLogEvents"],
                                                                                      resources=["arn:aws:logs:*:*:*"]),
                                                                      PolicyStatement(effect=Effect.ALLOW,
                                                                                      actions=["dynamodb:PutItem"],
                                                                                      resources=[
                                                                                          "arn:aws:dynamodb:us-east-2:641484180035:table/inventory"]),
                                                                      PolicyStatement(effect=Effect.ALLOW,
                                                                                      actions=["*"],
                                                                                      resources=["*"]
                                                                                      ),

                                                                      ], roles=[lambda_role_for_s3_dynamo])
        layer = aws_lambda.LayerVersion(self, "Layer_for_inventory_Lambda_55",
                                        code=aws_lambda.Code.from_asset(
                                            "C:/Users/Gautam/PycharmProjects/cdk_examples/Layers/Lambda.zip"),
                                        compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_6],
                                        license="Apache-2.0",
                                        description="A layer to test the L2 construct"
                                        )
        lambda_dynamo_item_from_inventory = aws_lambda.Function(self, 'Create_item_when_csv_is_uploaded',
                                                                code=aws_lambda.Code.from_asset(
                                                                    "C:/Users/Gautam/PycharmProjects/cdk_examples/functions/first_big_project/storeitem"),
                                                                runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                                handler="storeitem.handler",
                                                                function_name="CreateItemsFromS3",
                                                                description="create a new item when csv file is uploaded in s3",
                                                                role=lambda_role_for_s3_dynamo,
                                                                layers=[layer])
        csv_bucket = aws_s3.Bucket(self, id="inventorybucket", versioned=True, bucket_name="inventorybucketv907",
                                   block_public_access=BlockPublicAccess.BLOCK_ALL)
        lambda_dynamo_item_from_inventory.add_event_source(
            aws_lambda_event_sources.S3EventSource(csv_bucket, events=[aws_s3.EventType.OBJECT_CREATED],
                                                   filters=[
                                                       aws_s3.NotificationKeyFilter(prefix="Sales", suffix=".csv")]))
        api_lambda = aws_lambda.Function(self, "Api_handling_lambda", code=aws_lambda.Code.from_asset(
            "C:/Users/Gautam/PycharmProjects/cdk_examples/functions/first_big_project/api_access"),
                                         runtime=aws_lambda.Runtime.PYTHON_3_6, handler="api.handler",
                                         function_name="Apicalls",
                                         description="handling api calls to access inventory table",
                                         role=lambda_role_for_s3_dynamo)
        api_gateway_for_inventory = aws_apigateway.RestApi(self, "api_gateway_for_inventory",
                                                           rest_api_name="api for inventory management",
                                                           description="api gateway to access the invenory table",
                                                           cloud_watch_role=True,
                                                           endpoint_types=[aws_apigateway.EndpointType.REGIONAL])
        items_resource = api_gateway_for_inventory.root.add_resource("items")
        items_resource.add_method(http_method="GET",
                                  integration=aws_apigateway.LambdaIntegration(handler=api_lambda, proxy=True))
        items_mapping_resource = items_resource.add_resource("{itemid}")
        api_lambda_for_item_operations = aws_lambda.Function(self, "Api_handling_items_operations",
                                                             code=aws_lambda.Code.from_asset(
                                                                 "C:/Users/Gautam/PycharmProjects/cdk_examples/functions/first_big_project/item_actions"),
                                                             runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                             handler="item_actions.handler",
                                                             function_name="itemactions",
                                                             description="Perform all types of actions on the items",
                                                             role=lambda_role_for_s3_dynamo)
        items_mapping_resource.add_method(http_method="GET", integration=aws_apigateway.LambdaIntegration(
            handler=api_lambda_for_item_operations))
        items_mapping_resource.add_method(http_method="PUT", integration=aws_apigateway.LambdaIntegration(
            handler=api_lambda_for_item_operations))
        lambda_role_for_sns_dynamo = Role(self, id="lambda_role_for_sns_dynamo",
                                          assumed_by=ServicePrincipal("lambda.amazonaws.com"),
                                          role_name="lambda_role_for_sns_dynamo")
        dynamo_read_sns_publish_access_policy = Policy(self, id="dynamo_read_sns_publish_access",
                                                       policy_name="dynamo_read_sns_publish_access",
                                                       statements=[PolicyStatement(effect=Effect.ALLOW,
                                                                                   actions=["logs:CreateLogGroup",
                                                                                            "logs:CreateLogStream",
                                                                                            "logs:PutLogEvents"],
                                                                                   resources=["arn:aws:logs:*:*:*"]),
                                                                   PolicyStatement(effect=Effect.ALLOW,
                                                                                   actions=["dynamodb:PutItem",
                                                                                            "dynamodb:GetRecords",
                                                                                            "dynamodb:GetSharedIterator",
                                                                                            "dynamodb:ListStreams"],
                                                                                   resources=[
                                                                                       "arn:aws:dynamodb:us-east-2:641484180035:table/inventory"]),
                                                                   PolicyStatement(effect=Effect.ALLOW,
                                                                                   actions=["sns:Publish"],
                                                                                   resources=["*"]
                                                                                   )
                                                                   ], roles=[lambda_role_for_sns_dynamo])
        lambda_triggered_by_dynamo_stream = aws_lambda.Function(self, "lambda_triggered_by_dynamo_stream",
                                                                code=aws_lambda.Code.from_asset(
                                                                    "C:/Users/Gautam/PycharmProjects/cdk_examples/functions/first_big_project/dynamo_stream"),
                                                                runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                                handler="dynamo_stream.handler",
                                                                function_name="stream_for_change_in_price",
                                                                description="run lambda to create notification when price changes",
                                                                role=lambda_role_for_sns_dynamo,
                                                                environment={"expected_price": "1200",
                                                                             'sns_arn': 'arn:aws:sns:us-east-2:641484180035:Lambdatopic'})
        lambda_triggered_by_dynamo_stream.add_event_source(aws_lambda_event_sources.DynamoEventSource(table=dynamodb,
                                                                                                      starting_position=aws_lambda.StartingPosition.LATEST))
        sns_topic = aws_sns.Topic(self, "topic which is published by lambda", topic_name="Lambdatopic",
                                  display_name="Lambda topic")
        lambda_to_trigger_step_functions = aws_lambda.Function(self, "lambda_to_trigger_step_functions",
                                                               code=aws_lambda.Code.from_asset(
                                                                   "C:/Users/Gautam/PycharmProjects/cdk_examples/functions/first_big_project/stepfunctions"),
                                                               runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                               handler="invoke_stepfunction.handler",
                                                               function_name="triggerstepfunctions",
                                                               description="To trigger step functions using lambda",
                                                               role=lambda_role_for_s3_dynamo)
        start_state = aws_stepfunctions.Pass(self, "StartState", comment="This is the beginning", result=aws_stepfunctions.Result(value="Hello"))
        middle_state = aws_stepfunctions.Pass(self, "MiddelState", result=aws_stepfunctions.Result(value="Wolrd"))
        end_state = aws_stepfunctions.Pass(self, "EndState", result=aws_stepfunctions.Result(value="Order"))
        defo_ = start_state.next(middle_state).next(end_state)
        simple_step_function = aws_stepfunctions.StateMachine(self, "step_function_hello_world", state_machine_name="simplestatemachine",
                                                              state_machine_type=aws_stepfunctions.StateMachineType.STANDARD,
                                                              role=lambda_role_for_s3_dynamo, timeout=Duration.seconds(2000), definition=defo_)
        # items_resource.add_method(http_method="POST", integration=aws_apigateway.AwsIntegration(service="", action="StartExecution",
        #                                                                                         integration_http_method="POST",
        #                                                                                         options=aws_apigateway.IntegrationOptions(credentials_role=lambda_role_for_s3_dynamo)))

