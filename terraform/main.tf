terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Automatically fetch the latest Amazon Linux 2023 AMI in the selected region
data "aws_ami" "amazon_linux_2023" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# Security Group allowing SSH (22) and Streamlit Web Traffic (8501)
resource "aws_security_group" "loan_app_sg" {
  name        = "loan-approval-app-sg"
  description = "Allow SSH and Streamlit port 8501 inbound traffic"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit web application port"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "loan-approval-app-sg"
    Project = "loan-approval-app"
  }
}

# AWS EC2 Instance hosting the containerized Streamlit application
resource "aws_instance" "loan_app_server" {
  ami                    = data.aws_ami.amazon_linux_2023.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.loan_app_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              dnf update -y
              dnf install -y docker
              systemctl start docker
              systemctl enable docker
              docker pull ${var.docker_image}
              docker run -d -p 8501:8501 --restart unless-stopped --name loan-app ${var.docker_image}
              EOF

  tags = {
    Name    = "Loan-Approval-Streamlit-Server"
    Project = "loan-approval-app"
  }
}