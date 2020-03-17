provider "aws" {
  region = "eu-central-1"
}
terraform {
  backend "s3" {
  }
}

data "aws_route53_zone" "selected" {
  name = "${var.domain}"
}

module "service" {
  source                       = "git@github.com:dook/sfnf-infra.git//modules/terraform-aws-fargate"
  name_preffix                 = "${var.environment}-sfnf-portal"
  region                       = "eu-central-1"
  vpc_id                       = var.vpc_id
  availability_zones           = [var.azs]
  public_subnets_ids           = var.public_subnets
  private_subnets_ids          = var.private_subnets
  access_cidr_list             = ["0.0.0.0/0"]
  port_lb_external             = "443"
  container_name               = "${var.environment}-sfnf-portal"
  container_image              = "${var.ecr_registry}:${var.image_tag}"
  container_cpu                = 1024
  container_memory             = 2048
  container_memory_reservation = 2048
  container_port               = 8000
  internal                     = false
  certificate_arn              = var.certificate_arn
  environment = [
    {
      name  = "POSTGRES_HOST"
      value = var.postgres_host
    },
    {
      name  = "POSTGRES_USER"
      value = var.postgres_username
    },
    {
      name  = "POSTGRES_DB"
      value = "fh${var.environment}"
    },
    {
      name  = "POSTGRES_PASSWORD"
      value = var.postgres_password
    },
    {
      name  = "CORS_ORIGIN_ALLOW_ALL"
      value = var.cors_allow_all
    },
    {
      name  = "DEBUG"
      value = var.debug
    }
  ]
}

resource "aws_route53_record" "alb_public_web_endpoint" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = var.fqdn
  type    = "A"

  alias {
    name                   = module.service.lb_dns_name
    zone_id                = module.service.lb_zone_id
    evaluate_target_health = true
  }
}
