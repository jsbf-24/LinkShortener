import boto3
from datetime import datetime
import uuid
from app.config import settings

# Boto3 detectará automáticamente el rol IAM en EC2 o las credenciales locales de AWS CLI
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('urls-table')
def create_url_record(original_url: str):
    short_code = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    
    item = {
        "short_code": short_code,
        "original_url": original_url,
        "created_at": created_at
    }
    
    table.put_item(Item=item)
    return item

def get_url_record(short_code: str):
    response = table.get_item(Key={"short_code": short_code})
    return response.get("Item")