variable "access_key" {
    description = "AWS access key"
    type        = string
    default     = ""
}

variable "secret_key" {
    description = "AWS secret key"
    type        = string
    default     = ""
}

variable "author" {
  description = "Name of the operator. Used as a prefix to avoid name collision on resources."
  type        = string
  default     = ""
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = ""
}

variable "key_path" {
  description = "Key path for SSHing into EC2"
  type        = string
  default     = ""
}

variable "key_name" {
  description = "Key name for SSHing into EC2"
  type        = string
  default     = ""
}