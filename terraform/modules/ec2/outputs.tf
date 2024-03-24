output "instance_id" {
  value = aws_instance.example.id
}
output "ec2_instance_id" {
  value = aws_instance.example.id
}

output "ec2_instance_public_ip" {
  value = aws_instance.example.public_ip
}