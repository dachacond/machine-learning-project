provider "aws" {
  region = local.region
}

locals {
  name   = "minimal-cost-cluster"
  region = "us-east-1"

  vpc_cidr = "10.123.0.0/16"
  azs      = ["us-east-1a", "us-east-1b"]

  public_subnets  = ["10.123.1.0/24", "10.123.2.0/24"]

  tags = {
    Example = local.name
  }
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 4.0"

  name = local.name
  cidr = local.vpc_cidr

  azs             = local.azs
  public_subnets  = local.public_subnets
  
  map_public_ip_on_launch = true

  enable_nat_gateway = false  # NAT Gateway deshabilitado para reducir costos

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.15.1"

  cluster_name                   = local.name
  cluster_endpoint_public_access = true

  cluster_addons = {
    coredns    = { most_recent = true }
    kube-proxy = { most_recent = true }
    vpc-cni    = { most_recent = true }
    # Se eliminó el addon cluster-autoscaler ya que no es necesario
  }

  vpc_id = module.vpc.vpc_id
  # Al tener NAT deshabilitado, se utilizan las subredes públicas para el grupo de nodos y el plano de control
  subnet_ids               = module.vpc.public_subnets
  control_plane_subnet_ids = module.vpc.public_subnets

  eks_managed_node_groups = {
    "small-public-nodes" = {
      min_size     = 1
      max_size     = 2
      desired_size = 1

      instance_types = ["t3.small"]
      capacity_type  = "SPOT"  # Change to SPOT for significant savings
    }
  }

  # Configuración del mapeo de identidad IAM para GitHub Actions
  aws_auth_roles = [
    {
      rolearn  = "arn:aws:iam::796973493835:role/GitHubActionsRole"
      username = "githubactions"
      groups   = ["system:masters"]
    }
  ]

  tags = local.tags
}