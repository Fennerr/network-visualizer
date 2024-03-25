resource "aws_lb" "alb" {
  name               = "nv-public-alb"
  internal           = false
  load_balancer_type = "network"
  security_groups    = [var.elb_sg_id]
  subnets            = var.subnets

  enable_deletion_protection = false
}

## EC2

resource "aws_lb_target_group" "http_tg" {
  name     = "http-tg"
  port     = 80
  protocol = "TCP"
  vpc_id   = var.vpc_id

}

resource "aws_lb_listener" "front_end" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.http_tg.arn
  }
}

resource "aws_lb_target_group_attachment" "ec2_attach" {
  target_group_arn = aws_lb_target_group.http_tg.arn
  target_id        = var.ec2_instance_id
  port             = 80
}

## RDS

resource "aws_lb_listener" "rds_listener" {
  load_balancer_arn = aws_lb.alb.arn  # Ensure this references your ALB
  port              = 3389
  protocol          = "TCP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.rds_tg.arn
  }
}


resource "aws_lb_target_group" "rds_tg" {
  name     = "rds-tg"
  port     = 3389
  protocol = "TCP"
  target_type = "ip"
  vpc_id   = var.vpc_id

}

resource "aws_lb_target_group_attachment" "rds_attach" {
  target_group_arn = aws_lb_target_group.rds_tg.arn
  target_id        = var.rds_instance_ip
  port             = 3389
}