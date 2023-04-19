## Section 3: System Design - Design 2

### Architecture & Solution in AWS

Use cloud native serverless or managed services for scalability, HA, elasticity. That will increase cost, which we will deal later when necessary. 

### Architecture Diagram

![Architecture Diagram](architecture_diagram.png.png)

Utilize existing codebase and infra (Kafka streaming). The new API stack is build on top of Kafka streaming by adding Amazon Cognito for authentication and API Gateway, which directly ingest data into Kafka streaming, between the two it may need small Lambda function (not shown) for integration. 

Raw data is directly ingested into S3 input bucket from the Kafka streaming via Amazon Kinesis Data Streams service.  

Then existing image processing code is deployed as Lambda Function (it could also be Docker in EC2) producing output image and image metadata. 

Image metadata is stored in new AWS service, Timestream. Underlying is Dynamo db optimized for time series data and faster processing due to storage tiering, in memory for newly ingested data. Older data are move to slower storage medium and purge eventually. Timestream database may not enough for all analytical use case, but base on the 7 days retention period, it seems analytic query will be on aggregation data, which timestream handle very well then RMDB or NoSQL (Dynamo, MongoDB, parquet). 

Business Intelligence services offer two solution. Amazon QuickSight is used for frequent and no code analytics and dashboarding. For data scientist and expert analyst will used Jupyter Notebook power by Amazon Sagemaker. 

For security, untrusted pubnlic users are heavily layers and defends by AWS WAF and authenticated by Cognito. For internal user, services are available via VPN (likely site-to-site VPN) for easier and high performance connection. 

So far all services discussed are scalable and highly available. 