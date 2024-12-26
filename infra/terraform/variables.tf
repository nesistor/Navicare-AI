variable "repo_name" {
  description = "The name of the Artifact Registry repository."
  type        = string
}

variable "region" {
  description = "The GCP region for resources."
  type        = string
  default     = "us-central1"
}

variable "project_id" {
  description = "The GCP project ID."
  type        = string
}