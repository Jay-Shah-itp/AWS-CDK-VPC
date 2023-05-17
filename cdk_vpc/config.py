from aws_cdk.aws_ec2 import RouterType

VPC = 'cdk-custom-vpc'

VPC_CIDR = '10.0.0.0/16'

INTERNET_GATEWAY = 'cdk-internet-gateway'

REGION = 'us-east-1'

PUBLIC_ROUTE_TABLE = 'public-route-table'

ROUTE_TABLES_ID_TO_ROUTES_MAP = {
    PUBLIC_ROUTE_TABLE: [
        {
            'destination_cidr_block': '0.0.0.0/0',
            'gateway_id': INTERNET_GATEWAY,
            'router_type': RouterType.GATEWAY
        }
    ],
}

PUBLIC_SUBNET = 'public-subnet'
PRIVATE_SUBNET = 'private-subnet'

SUBNET_CONFIGURATION = {
    PUBLIC_SUBNET: {
        'availability_zone': 'us-east-1a', 'cidr_block': '10.0.1.0/24', 'map_public_ip_on_launch': True,
        'route_table_id': PUBLIC_ROUTE_TABLE
    },
    PRIVATE_SUBNET: {
        'availability_zone': 'us-east-1b', 'cidr_block': '10.0.2.0/24', 'map_public_ip_on_launch': False,
        'route_table_id': PUBLIC_ROUTE_TABLE
    }
}


