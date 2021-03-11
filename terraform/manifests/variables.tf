variable "billing_account" {
  default     = null
  type        = string
  description = "The name of your billing account. Case-sensitive."
}

variable "name_prefix" {
  type        = string
  description = "Name prefix for project name. Case-sensitive."
}

variable "folder_id" {
  type        = string
  description = "Folder ID to spin up project under."
}

variable "state_bucket_name" {
  type        = string
  description = "The name of your bucket to store the state file. Case-sensitive."
}

variable "bucket_name" {
  type        = string
  description = "The name of your bucket to store the random logs. Case-sensitive."
}

variable "region" {
  default     = "us-central1"
  type        = string
  description = "The name of your bucket to store the random logs. Case-sensitive."
}