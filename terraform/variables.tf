# Variables are like settings you can customise
# Instead of hardcoding values in main.tf, we define them here
# and reuse them everywhere

variable "app_namespace" {
  # This is the Kubernetes namespace where our app will live
  # Think of namespace like a folder inside Kubernetes
  description = "Kubernetes namespace for the app"
  type        = string
  default     = "devmind-ai"
}

variable "environment" {
  # Tells our app which environment it is running in
  # Can be changed to "staging" or "production" later
  description = "Deployment environment"
  type        = string
  default     = "development"
}

variable "app_version" {
  # Version of our app — updated automatically by CI/CD pipeline
  description = "App version"
  type        = string
  default     = "1.0.0"
}
