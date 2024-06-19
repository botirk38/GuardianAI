

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.8.1"
  
  name = "smarguardian-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["eu-west-2a", "eu-west-2b"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.3.0/24", "10.0.4.0/24"]
  
  enable_nat_gateway = true

}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "smartguardian-cluster"
  cluster_version = "1.21"
  
  vpc_id        = module.vpc.vpc_id
  subnet_ids    = module.vpc.private_subnets

  eks_managed_node_groups = {
    managed_group = {
      instance_types = ["t3.medium"]
      desired_capacity = 3
      max_capacity     = 4
      min_capacity     = 2
    }
  }
}

module "eks_addons" {
  source  = "aws-ia/eks-blueprints-addons/aws"
  version = "~> 1.16.3"

  cluster_name     = module.eks.cluster_name
  cluster_endpoint = module.eks.cluster_endpoint
  cluster_version  = module.eks.cluster_version
  oidc_provider_arn = module.eks.oidc_provider

  eks_addons = {
    vpc-cni = {
      most_recent = true
    }
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
   
  }

  tags = local.tags
}

locals {
  tags = {
    Name        = "example"
    Environment = "production"
  }
}

