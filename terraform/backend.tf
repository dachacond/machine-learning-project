terraform {
  backend "s3" {
    bucket  = "mlapi2-terraform-state"
    region  = "us-east-1"
    key     = "terraform.tfstate"
    encrypt = true
  }
  
  required_version = ">=0.13.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.0.0, < 6.0.0"
    }
  }
}
