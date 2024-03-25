variable "vpc_id" {}
variable "subnets" {
  type = list(string)
}

variable "elb_sg_id" {
  description = "The ID of the security group for the Elastic Load Balancer"
  type        = string
}

variable "ec2_instance_id" {
  description = "The ID of the EC2 instance to which the load balancer will route traffic"
  type        = string
}

variable "rds_instance_ip" {
  description = "The IP address of the RDS instance to which the load balancer will route traffic"
  type        = string
}
