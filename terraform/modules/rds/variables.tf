variable "allocated_storage" {}
variable "engine" {}
variable "engine_version" {}
variable "instance_class" {}
variable "db_name" {}
variable "db_username" {}
variable "db_password" {}

variable "rds_subnet_group_name" {
  description = "The name of the RDS subnet group"
    type        = string
}

variable "rds_sg_id" {
  description = "The security group ID for the RDS instance"
    type        = string
}