
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.40.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = ">= 2.0.0"
    }
  }

  required_version = "1.8.5"
}

provider "aws" {
  region = "eu-west-2"
}
