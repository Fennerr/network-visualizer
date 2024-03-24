resource "aws_instance" "example" {
  ami           = length(var.ami) > 0 ? var.ami : data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = aws_key_pair.deployer_key.key_name

  vpc_security_group_ids = [var.ec2_sg_id]
  subnet_id     = var.subnet_id

  user_data = file("${path.module}/ec2_userdata.sh")

  tags = {
    Name = var.instance_name
  }
}

resource "aws_key_pair" "deployer_key" {
  key_name   = "nv-deployer-key"
  public_key = file(var.public_key_path)
}