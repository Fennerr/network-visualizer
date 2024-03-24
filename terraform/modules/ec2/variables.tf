variable "ami" {
    description = "The AMI ID for the EC2 instance"
    type        = string
    default     = ""
}
variable "instance_type" {}
# variable "key_name" {}
variable "instance_name" {}

variable "public_key_path" {
  description = "Path to the public SSH key to be used for EC2 instances"
  type        = string
  # No default value is set, as it will be provided via an environment variable
}

variable "subnet_id" {
  description = "The subnet ID where the EC2 instance will be launched"
    type        = string
}

variable "ec2_sg_id" {
  description = "The security group ID for the EC2 instance"
    type        = string
}
