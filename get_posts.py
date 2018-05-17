import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    postId = event["postId"]
    
    try :
        tableName = os.environ['DB_TABLE_NAME']
    
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(tableName)
        
        if (postId == "*") :
            items = table.scan()
        else :
            items = table.query(
                KeyConditionExpression = Key('id').eq(postId)
            )
          
        return items["Items"]
    except KeyError as keyEx :
        print(keyEx)
        msg = "ERROR: Need Environment Var : DB_TABLE_NAME"
        print(msg)
        return msg