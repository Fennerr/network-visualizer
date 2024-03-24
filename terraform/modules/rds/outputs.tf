output "db_instance_endpoint" {
  value = aws_db_instance.example.endpoint
}

output "rds_instance_ip" {
  value = data.dns_a_record_set.rds.addrs[0]
}
