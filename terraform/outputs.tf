output "rds_instance_ip" {
  value = module.rds.rds_instance_ip
}

output "db_instance_endpoint" {
  value = module.rds.db_instance_endpoint
}

output "elb_public_dns" {
  value = module.elb.elb_public_dns
}

output "ec2_instance_public_ip" {
  value = module.ec2.ec2_instance_public_ip
}