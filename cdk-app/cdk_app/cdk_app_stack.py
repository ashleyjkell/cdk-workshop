from aws_cdk import (
Stack, 
aws_s3 as s3  
)

class CdkAppStack(Stack):

    def __init__(self, scope, id, **kwargs):
        super().__init__(scope, id, **kwargs)

        s3.Bucket(
        self, 
        "MyBucket",
        versioned=True
        )