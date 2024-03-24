locals {
  hostname = split(":", aws_db_instance.example.endpoint)[0]
}

data "dns_a_record_set" "rds" {
  host = local.hostname
}
