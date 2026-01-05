resource "aws_db_subnet_group" "rds_sg" {
  name       = "asterra-db-subnet-group"
  subnet_ids = [var.private_subnet_id]
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"
  db_name              = "asterra_db"
  username             = "asterra_admin"
  password             = var.db_password
  db_subnet_group_name = aws_db_subnet_group.rds_sg.name
  skip_final_snapshot  = true
  publicly_accessible  = false
}