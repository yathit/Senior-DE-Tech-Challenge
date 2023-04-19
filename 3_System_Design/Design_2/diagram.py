from diagrams import Cluster, Diagram, Edge
from diagrams.aws.analytics import KinesisDataStreams, Quicksight
from diagrams.aws.compute import EC2, LambdaFunction
from diagrams.aws.general import InternetGateway
from diagrams.aws.ml import SagemakerNotebook, Sagemaker
from diagrams.aws.mobile import APIGateway
from diagrams.aws.security import WAF, Cognito
from diagrams.aws.storage import S3
from diagrams.aws.network import ClientVpn, VpnGateway
from diagrams.aws.database import Timestream
from diagrams.onprem.client import Users
from diagrams.onprem.compute import Server
from diagrams.onprem.queue import Kafka

graph_attr = {
    "fontsize": "32"
}

with Diagram(name="Image processing web application", filename='architecture_diagram',
             show=True, outformat=['png', 'dot'], graph_attr=graph_attr):
    users = Users(label='Users')
    analysts = Users(label="Analysts")
    vpn_client = ClientVpn(label='VPN')

    waf = WAF(label='AWS WAF')

    with Cluster('VPC Public'):
        auth = Cognito('Cognito Authentication')
        api_gateway = APIGateway('API Gateway')

        ig = InternetGateway('Internet Gateway')
        client = Server(label='Web Application')
        kafka = Kafka(label='Kafka Streaming')
        ds = KinesisDataStreams('Kinesis Data Streams')

        with Cluster('Business Intelligent'):
            vpn_gateway = VpnGateway(label='VPN Gateway')
            qs = Quicksight('QuickSight')
            notebook = SagemakerNotebook('Sagemaker Notebook')

    with Cluster('VPC Private'):
        sgm = Sagemaker('Sagemaker\nTraining Job, Models')
        input_bucket = S3(label='Input bucket\nLife cycle rules: 7 days')
        image_processor = LambdaFunction(label='Image processor')
        output_bucket = S3(label='Output bucket\nLife cycle rules: 7 days')
        db = Timestream('Amazon Timestream\nFor image metadata\nExpired after 7 days')

    users >> Edge(label='Image/HTTP') >> waf >> ig >> auth >> api_gateway >> ds
    client >> kafka >> ds >> input_bucket >> image_processor

    output_bucket << image_processor
    db << image_processor
    analysts >> vpn_client >> vpn_gateway
    sgm << output_bucket
    vpn_gateway << notebook << sgm << db
    vpn_gateway << qs << db
