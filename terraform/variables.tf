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
