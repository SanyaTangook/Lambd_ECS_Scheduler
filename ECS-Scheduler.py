import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('ecs')

def lambda_handler(event, context):
    clusters = list(event.keys())
    clusters.remove('service_status')
    
    status = 1 if event['service_status'].lower() == 'on' else 0
    
    for cluster in clusters:
        for service_name in event[cluster]:
            response = client.update_service(
                cluster=cluster,
                service=service_name,
                desiredCount = status
                )
                
            logger.info("Updated {0} service in {1} cluster with desire count set to {2} tasks".format(service_name, cluster, event['service_status']))

    
    return {
        'statusCode': 200,
        'new_desired_count': event['service_status']
    }
    
    
    """
    json file 
    {
        NameCluster : [
            NameSerice1 ,
            NameSerice2 
        ],
        service_status : ` on ` OR ` off `
    }
    """