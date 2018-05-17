import os
import uuid
import boto3

def lambda_handler(event, context):
    recordId = str(uuid.uuid4())
    
    text = event['text']
    voice = event['voice']
    
    print('*Input Text*=', text)
    print('*Selected Voice*=', voice)
    
    # Generate record in DynamoDB
    try :
        tableName = os.environ['DB_TABLE_NAME']
        print('*DynamoDB TableName*=', tableName)

        # Need client just to access the Exception
        dynamodb_client = boto3.client('dynamodb')
        
        dynamodb = boto3.resource('dynamodb')
        
        try :
            # table = dynamodb_client.list_tables()[tableName]
            table = dynamodb.Table(tableName)
            
            table.put_item (
                Item= {
                    'id': recordId,
                    'text': text,
                    'voice': voice,
                    'status': 'PROCESSING'
                }
            )
            print('Generated new DynamoDB record, ID: ' + recordId)
        except dynamodb_client.exceptions.ResourceNotFoundException as tableNotFoundEx:
            return ('ERROR: Unable to locate DynamoDB table: ', tableName)
        
    except KeyError as dynamoDBKeyError:
        msg = 'ERROR: Need DynamoDB Environment Var: DB_TABLE_NAME'
        print(dynamoDBKeyError)
        return msg;
    
    
    # Send Notificaiton to SNS
    try :
        topicName = os.environ['SNS_TOPIC_ARN']
        print('*SNS TopicName*=', topicName)
        
        sns_client = boto3.client('sns')
        
        sns_client.publish(
            TopicArn = topicName,
            Message = recordId
        )
        
        print('Generated new SNS message, ID: ' + recordId)
    except KeyError as snsKeyError:
        msg = 'ERROR: Need SNS Environment Var: SNS_TOPIC_NAME'
        print(snsKeyError)
        return msg;
        
        
    return recordId