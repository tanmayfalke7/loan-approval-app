variable "aws_region" {
  description = "AWS region where the EC2 instance will be provisioned"
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type (Free Tier eligible)"
  type        = string
  default     = "t3.micro"
}

variable "docker_image" {
  description = "Docker Hub image to deploy on the EC2 instance"
  type        = string
  default     = "tanmayfalke7/loan-approval-app:v1"
}