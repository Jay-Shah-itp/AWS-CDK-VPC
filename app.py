#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_vpc.cdk_vpc_stack import CdkVpcStack


app = cdk.App()
CdkVpcStack(app, "cdk-vpc")

app.synth()
