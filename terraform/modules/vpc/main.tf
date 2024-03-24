resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  enable_dns_support = true
  enable_dns_hostnames = true
  tags = {
    Name = "MainVPC"
  }
}

resource "aws_subnet" "public" {
  count = length(var.public_subnet_cidrs)

  cidr_block = var.public_subnet_cidrs[count.index]
  availability_zone = element(var.availability_zones, count.index)
  vpc_id = aws_vpc.main.id

  # Additional configuration...
}

# resource "aws_subnet" "public" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = var.public_subnet_cidr
#   map_public_ip_on_launch = true
#   availability_zone = var.availability_zone

#   tags = {
#     Name = "PublicSubnet"
#   }
# }

# resource "aws_subnet" "public_two" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = var.public_subnet_cidr
#   map_public_ip_on_launch = true
#   availability_zone = var.availability_zone_two

#   tags = {
#     Name = "PublicSubnetBackup"
#   }
# }

# resource "aws_subnet" "private" {
#   vpc_id            = aws_vpc.main.id
#   cidr_block        = var.private_subnet_cidr
#   availability_zone = var.availability_zones[0]

#   tags = {
#     Name = "PrivateSubnet"
#   }
# }

resource "aws_subnet" "private" {
  count = length(var.private_subnet_cidrs)

  cidr_block = var.private_subnet_cidrs[count.index]
  availability_zone = element(var.availability_zones, count.index)
  vpc_id = aws_vpc.main.id

  # Additional configuration...
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "main-igw"
  }
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = aws_subnet.private[*].id
}