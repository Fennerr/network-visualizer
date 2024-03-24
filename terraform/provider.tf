provider "aws" {
  region = "eu-west-1"
}

terraform {
  required_providers {
    dns = {
      source  = "hashicorp/dns"
      version = "~> 3.0"
    }
  }
}

provider "dns" {
  # Configuration options
}
