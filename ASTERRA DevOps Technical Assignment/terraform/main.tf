provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
}

module "s3" {
  source      = "./modules/S3"
  bucket_name = var.ingestion_bucket_name
}

module "rds" {
  source            = "./modules/RDS"
  db_password       = var.db_password
  vpc_id            = module.vpc.vpc_id
  private_subnet_id = module.vpc.private_subnet_id
}