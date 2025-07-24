
# Terraform configuration for hosting large files on AWS

# 1. S3 Bucket for File Storage
# This S3 bucket will be the primary storage for your 4TB of files.
# It's scalable, durable, and cost-effective for large amounts of data.

resource "aws_s3_bucket" "file_storage" {
  bucket = "large-file-storage-bucket-${random_pet.this.id}"

  tags = {
    Name      = "Large File Storage"
    ManagedBy = "Gemini"
  }
}

resource "aws_s3_bucket_versioning" "file_storage_versioning" {
  bucket = aws_s3_bucket.file_storage.id
  versioning_configuration {
    status = "Enabled"
  }
}

# 2. IAM Role for EC2 Instance
# This IAM role will be assumed by our EC2 instance, granting it
# permissions to access the S3 bucket without needing hard-coded credentials.

resource "aws_iam_role" "ec2_s3_access_role" {
  name = "ec2-s3-access-role-${random_pet.this.id}"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "EC2 S3 Access Role"
  }
}

# 3. IAM Policy for S3 Access
# This policy defines the specific permissions the EC2 instance has on the S3 bucket.
# It allows listing the bucket and performing all object actions (read, write, delete).

resource "aws_iam_policy" "s3_access_policy" {
  name        = "s3-access-policy-${random_pet.this.id}"
  description = "Allows EC2 instance to access the file storage S3 bucket"

  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action   = [
          "s3:ListBucket"
        ],
        Effect   = "Allow",
        Resource = aws_s3_bucket.file_storage.arn
      },
      {
        Action   = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Effect   = "Allow",
        Resource = "${aws_s3_bucket.file_storage.arn}/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_s3_policy" {
  role       = aws_iam_role.ec2_s3_access_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ec2-instance-profile-${random_pet.this.id}"
  role = aws_iam_role.ec2_s3_access_role.name
}

# 4. Security Group for the EC2 Instance
# This security group acts as a virtual firewall.
# IMPORTANT: For now, it allows SSH access from any IP address (0.0.0.0/0).
# For production use, you should restrict this to your own IP address for security.

resource "aws_security_group" "ec2_sg" {
  name        = "ec2-ssh-access-sg-${random_pet.this.id}"
  description = "Allow SSH access to EC2 instance"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "EC2 SSH Access"
  }
}

# 5. EC2 Instance
# This is the server you will use to access and manage your files in S3.
# It uses the latest Amazon Linux 2 AMI and a small instance type.

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_instance" "file_manager_instance" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = "t2.micro" # Sufficient for management tasks, and free-tier eligible

  iam_instance_profile = aws_iam_instance_profile.ec2_profile.name
  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  # IMPORTANT: Replace "your-key-name" with the name of your EC2 key pair.
  # You will need this key to SSH into the instance.
  key_name = "your-key-name"

  tags = {
    Name = "File Manager Instance"
  }
}

# 6. Outputs
# These outputs will display the S3 bucket name and the public IP of your
# EC2 instance after you apply the configuration.

output "s3_bucket_name" {
  description = "The name of the S3 bucket for file storage."
  value       = aws_s3_bucket.file_storage.bucket
}

output "ec2_instance_public_ip" {
  description = "The public IP address of the file manager EC2 instance."
  value       = aws_instance.file_manager_instance.public_ip
}
