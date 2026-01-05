variable "aws_region" {
  description = "The AWS region to deploy to"
  type        = string
  default     = "us-east-1"
}

variable "ingestion_bucket_name" {
  description = "Name of the S3 bucket for ingestion"
  type        = string
}

variable "db_password" {
  description = "Password for the RDS database"
  type        = string
  sensitive   = true
}