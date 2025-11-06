from constructs import Construct
from aws_cdk import Stack, RemovalPolicy, aws_s3 as s3
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_elasticloadbalancingv2 as elbv2

class AppStack(Stack):
    def __init__ (self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Example resource: S3 Bucket
        bucket = s3.Bucket(self, 
                           "PimaryBucket",
                           versioned=True,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
                           enforce_ssl=True,
                           removal_policy=RemovalPolicy.DESTROY,
                           auto_delete_objects=True
                           )
        
        # I would like to create a load balancer here but I am not sure how to import the necessary modules and set it up.
        # Please provide guidance on how to implement an Application Load Balancer in this stack.
         
        vpc = ec2.Vpc(self, "MyPipelineVpc", max_azs=2)
        lb = elbv2.ApplicationLoadBalancer(self, "MyPipelineALB",
                                           vpc=vpc,
                                           internet_facing=True)
        listener = lb.add_listener("Listener", port=80)
        listener.add_action("DefaultAction",
                            action=elbv2.ListenerAction.fixed_response(
                                status_code=200,
                                content_type="text/plain",
                                message_body="Hello, World!"
                            ))
        # The load balancer is set up to respond with "Hello, World!" on port 80.
        # You can test the load balancer by accessing its DNS name in a web browser or using curl.
        # The DNS name can be found in the AWS Management Console under the EC2 service,
        # in the Load Balancers section.
        