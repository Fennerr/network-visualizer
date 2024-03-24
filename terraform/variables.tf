# RDS Variables
variable "allocated_storage" {}
variable "engine" {}
variable "engine_version" {}
variable "instance_class" {}
variable "db_name" {}
variable "db_username" {}
variable "rds_db_password" {}

# EC2 Variables
# variable "ami" {}
variable "instance_type" {}
variable "instance_name" {}
# variable "key_name" {}
variable "public_key_path" {
  # No default value is set, as it will be provided via an environment variable
}

# ELB Variables
# variable "vpc_id" {}
# variable "subnets" {
#   type = list(string)
# }
