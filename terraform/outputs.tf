output "ec2_instance_id" {
  description = "ID of the provisioned EC2 instance"
  value       = aws_instance.loan_app_server.id
}

output "ec2_public_ip" {
  description = "Public IPv4 address of the EC2 instance"
  value       = aws_instance.loan_app_server.public_ip
}

output "application_url" {
  description = "Live URL for the Streamlit Loan Approval application"
  value       = "http://${aws_instance.loan_app_server.public_ip}:8501"
}