# Project Configuration
project_name = "video-streaming-platform"
environment  = "dev"

# AWS Configuration
aws_region = "us-east-1"

# Network Configuration
vpc_cidr = "10.0.0.0/16"

# Database Configuration
db_name           = "video_streaming_db"
db_username       = "dbadmin"
db_password       = "ChangeMe123!SecurePassword"  # CHANGE THIS IN PRODUCTION
db_instance_class = "db.t3.medium"
db_allocated_storage     = 100
db_max_allocated_storage = 1000
db_multi_az             = false  # Set to true for production

# Storage Configuration
s3_lifecycle_enabled        = true
s3_ia_transition_days      = 30
s3_glacier_transition_days = 90

# Lambda Configuration
lambda_timeout     = 30
lambda_memory_size = 256

# Monitoring Configuration
cloudwatch_log_retention_days = 14

# Cost Optimization Tags
cost_center = "engineering"
owner       = "platform-team"

# Security Configuration
enable_deletion_protection = false  # Set to true for production
backup_retention_period   = 7

# API Gateway Configuration
api_throttle_rate_limit  = 1000
api_throttle_burst_limit = 2000

# Example Production Configuration (commented out)
# Uncomment and modify for production deployment:

# project_name = "video-streaming-platform"
# environment  = "production"
# aws_region   = "us-east-1"
# 
# # Production Network Settings
# vpc_cidr = "10.0.0.0/16"
# 
# # Production Database Settings
# db_name                  = "video_streaming_prod_db"
# db_username              = "proddbadmin"
# db_password              = "SuperSecureProductionPassword123!"
# db_instance_class        = "db.r5.xlarge"
# db_allocated_storage     = 500
# db_max_allocated_storage = 5000
# db_multi_az             = true
# 
# # Production Storage Settings
# s3_lifecycle_enabled        = true
# s3_ia_transition_days      = 30
# s3_glacier_transition_days = 90
# 
# # Production Lambda Settings
# lambda_timeout     = 60
# lambda_memory_size = 512
# 
# # Production Monitoring
# cloudwatch_log_retention_days = 90
# 
# # Production Security
# enable_deletion_protection = true
# backup_retention_period   = 30
# 
# # Production API Settings
# api_throttle_rate_limit  = 5000
# api_throttle_burst_limit = 10000
# 
# # Production Tags
# cost_center = "video-platform"
# owner       = "video-platform-team"