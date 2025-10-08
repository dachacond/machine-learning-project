variable "github_actions_role_arn" {
  description = "ARN del role que GitHub Actions debe asumir, p.ej. arn:aws:iam::123456789012:role/GitHubActionsRole"
  type        = string
  default     = ""
}

variable "region" {
  description = "AWS region to deploy"
  type        = string
  default     = "us-east-1"
}

variable "kms_key_arn" {
  description = "ARN of pre-created KMS key to use for resources (set to empty to allow module to create keys)"
  type        = string
  default     = ""
}
