from constructs import Construct
from aws_cdk import Stack
from aws_cdk.aws_ec2 import Vpc, CfnRouteTable, RouterType, CfnRoute, CfnInternetGateway, CfnVPCGatewayAttachment, \
    CfnSubnet, CfnSubnetRouteTableAssociation
from . import config


class CdkVpcStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = Vpc(
            self, config.VPC, cidr=config.VPC_CIDR, nat_gateways=0, subnet_configuration=[]
        )

        self.internet_gateway = self.attach_internet_gateway()

        self.subnet_id_to_subnet_map = {}
        self.route_table_id_to_route_table_map = {}

        self.create_route_tables()

        self.create_subnets()
        self.create_subnet_route_table_associations()

        self.create_routes()

    def create_route_tables(self):
        for route_table_id in config.ROUTE_TABLES_ID_TO_ROUTES_MAP:
            self.route_table_id_to_route_table_map[route_table_id] = CfnRouteTable(
                self, route_table_id, vpc_id=self.vpc.vpc_id, tags=[{'key': 'Name', 'value': route_table_id}]
            )

    def create_routes(self):
        for route_table_id, routes in config.ROUTE_TABLES_ID_TO_ROUTES_MAP.items():
            for i in range(len(routes)):
                route = routes[i]

                kwargs = {
                    **route,
                    'route_table_id': self.route_table_id_to_route_table_map[route_table_id].ref,
                }

                if route['router_type'] == RouterType.GATEWAY:
                    kwargs['gateway_id'] = self.internet_gateway.ref

                del kwargs['router_type']

                CfnRoute(self, f'{route_table_id}-route-{i}', **kwargs)

    def attach_internet_gateway(self) -> CfnInternetGateway:
        internet_gateway = CfnInternetGateway(self, config.INTERNET_GATEWAY)
        CfnVPCGatewayAttachment(self, 'internet-gateway-attachment', vpc_id=self.vpc.vpc_id,
                                internet_gateway_id=internet_gateway.ref)

        return internet_gateway

    def create_subnets(self):
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION.items():
            subnet = CfnSubnet(
                self, subnet_id, vpc_id=self.vpc.vpc_id, cidr_block=subnet_config['cidr_block'],
                availability_zone=subnet_config['availability_zone'], tags=[{'key': 'Name', 'value': subnet_id}],
                map_public_ip_on_launch=subnet_config['map_public_ip_on_launch'],
            )

            self.subnet_id_to_subnet_map[subnet_id] = subnet

    def create_subnet_route_table_associations(self):
        for subnet_id, subnet_config in config.SUBNET_CONFIGURATION.items():
            route_table_id = subnet_config['route_table_id']

            CfnSubnetRouteTableAssociation(
                self, f'{subnet_id}-{route_table_id}', subnet_id=self.subnet_id_to_subnet_map[subnet_id].ref,
                route_table_id=self.route_table_id_to_route_table_map[route_table_id].ref
            )

 