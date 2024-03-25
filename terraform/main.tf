module "vpc" {
  source = "./modules/vpc"
  vpc_cidr = "10.0.0.0/16"
  public_subnet_cidrs = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
  availability_zones = ["eu-west-1a", "eu-west-1b"]
}

module "ec2" {
    source        = "./modules/ec2"
    # Variables
    instance_type = var.instance_type
    public_key_path = var.public_key_path
    instance_name = var.instance_name
    # Module outputs
    subnet_id = module.vpc.public_subnet_id
    ec2_sg_id = module.vpc.ec2_sg_id
}

module "rds" {
    source            = "./modules/rds"
    allocated_storage = var.allocated_storage
    engine            = var.engine
    engine_version    = var.engine_version
    instance_class    = var.instance_class
    db_name           = var.db_name
    db_username       = var.db_username
    db_password       = var.rds_db_password

    rds_subnet_group_name = module.vpc.rds_subnet_group_name
    rds_sg_id             = module.vpc.rds_sg_id
}

module "elb" {
    source = "./modules/elb"
    vpc_id = module.vpc.vpc_id
    subnets = module.vpc.subnets
    ec2_instance_id = module.ec2.ec2_instance_id
    rds_instance_ip = module.rds.rds_instance_ip
    elb_sg_id = module.vpc.elb_sg_id
}

