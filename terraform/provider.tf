provider "aws" {
  region = "eu-west-1"
}

terraform {
  required_providers {
    dns = {
      source  = "hashicorp/dns"
      version = "~> 3.0"
    }
    publicip = {
      source  = "nxt-engineering/publicip"
      version = "~> 0.0.9"
    }
  }
}

provider "dns" {
  # Configuration options
}

provider "publicip" {
  provider_url = "https://ifconfig.co/" # optional
  timeout      = "10s"                  # optional

  # 1 request per 500ms
  rate_limit_rate  = "500ms" # optional
  rate_limit_burst = "1"     # optional
}