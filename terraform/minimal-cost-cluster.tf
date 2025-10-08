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

  # cluster_encryption_config eliminado para no usar KMS

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
      rolearn  = var.github_actions_role_arn
      username = "githubactions"
      groups   = ["system:masters"]
    }
  ]

  tags = local.tags
  # Use an existing KMS key (provided via var.kms_key_arn) for cluster secret encryption and
  # CloudWatch log group encryption. Disable creation of a new KMS key in the module.
  create_kms_key = false
  cluster_encryption_config = {
    resources = ["secrets"]
    provider_key_arn = var.kms_key_arn
  }
  # If you want CloudWatch log groups encrypted with the same key, set this as well
  # Use the KeyId (not the ARN) when providing a key for CloudWatch log group encryption.
  # Pass `var.kms_key_id` (extract KeyId from ARN if necessary) so the module can use it.
  cloudwatch_log_group_kms_key_id = var.kms_key_id
}