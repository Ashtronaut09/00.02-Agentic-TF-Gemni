import json
import os
import logging
import boto3
from datetime import datetime
import uuid

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')

def handler(event, context):
    """
    Lambda function handler for video streaming platform API
    Handles basic CRUD operations for video metadata
    """
    try:
        # Log the incoming event
        logger.info(f"Received event: {json.dumps(event, default=str)}")
        
        # Extract HTTP method and path
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '')
        
        # CORS headers
        headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,PUT,DELETE'
        }
        
        # Handle preflight OPTIONS request
        if http_method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight successful'})
            }
        
        # Route the request based on method and path
        if path == '/videos' and http_method == 'GET':
            return handle_get_videos(event, headers)
        elif path == '/videos' and http_method == 'POST':
            return handle_post_video(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Not Found',
                    'message': f'Path {path} with method {http_method} not found'
                })
            }
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            })
        }

def handle_get_videos(event, headers):
    """
    Handle GET /videos - List videos
    """
    try:
        # Get environment variables
        staging_bucket = os.environ.get('STAGING_BUCKET')
        distribution_bucket = os.environ.get('DISTRIBUTION_BUCKET')
        
        if not staging_bucket or not distribution_bucket:
            raise ValueError("Required environment variables not set")
        
        # List objects in distribution bucket (processed videos)
        response = s3_client.list_objects_v2(
            Bucket=distribution_bucket,
            MaxKeys=100
        )
        
        videos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                videos.append({
                    'id': obj['Key'].split('/')[-1].split('.')[0] if '/' in obj['Key'] else obj['Key'].split('.')[0],
                    'filename': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'url': f"https://{distribution_bucket}.s3.amazonaws.com/{obj['Key']}"
                })
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'videos': videos,
                'count': len(videos),
                'bucket': distribution_bucket,
                'timestamp': datetime.utcnow().isoformat()
            })
        }
        
    except Exception as e:
        logger.error(f"Error in handle_get_videos: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Failed to retrieve videos',
                'message': str(e)
            })
        }

def handle_post_video(event, headers):
    """
    Handle POST /videos - Create presigned URL for video upload
    """
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        filename = body.get('filename')
        content_type = body.get('content_type', 'video/mp4')
        
        if not filename:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({
                    'error': 'Bad Request',
                    'message': 'filename is required'
                })
            }
        
        # Get environment variables
        staging_bucket = os.environ.get('STAGING_BUCKET')
        
        if not staging_bucket:
            raise ValueError("STAGING_BUCKET environment variable not set")
        
        # Generate unique key for the upload
        video_id = str(uuid.uuid4())
        file_extension = filename.split('.')[-1] if '.' in filename else 'mp4'
        s3_key = f"uploads/{video_id}.{file_extension}"
        
        # Generate presigned URL for upload
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': staging_bucket,
                'Key': s3_key,
                'ContentType': content_type
            },
            ExpiresIn=3600  # 1 hour
        )
        
        # Create video metadata
        video_metadata = {
            'id': video_id,
            'original_filename': filename,
            's3_key': s3_key,
            'bucket': staging_bucket,
            'content_type': content_type,
            'status': 'pending_upload',
            'created_at': datetime.utcnow().isoformat()
        }
        
        return {
            'statusCode': 201,
            'headers': headers,
            'body': json.dumps({
                'video': video_metadata,
                'upload_url': presigned_url,
                'expires_in': 3600,
                'instructions': {
                    'method': 'PUT',
                    'headers': {
                        'Content-Type': content_type
                    },
                    'note': 'Use the upload_url to upload your video file directly to S3'
                }
            })
        }
        
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({
                'error': 'Bad Request',
                'message': 'Invalid JSON in request body'
            })
        }
    except Exception as e:
        logger.error(f"Error in handle_post_video: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Failed to create upload URL',
                'message': str(e)
            })
        }

def get_database_connection():
    """
    Get database connection (placeholder for future database integration)
    """
    # Database connection details from environment variables
    db_host = os.environ.get('DB_HOST')
    db_name = os.environ.get('DB_NAME')
    db_username = os.environ.get('DB_USERNAME')
    db_password = os.environ.get('DB_PASSWORD')
    
    # TODO: Implement actual database connection using psycopg2 or similar
    # This is a placeholder for future implementation
    logger.info(f"Database connection configured for {db_host}:{db_name}")
    
    return None