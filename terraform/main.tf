# This file defines all the Kubernetes resources
# Terraform will create everything written here automatically
# Run: terraform init → terraform plan → terraform apply

terraform {
  # Tell Terraform which plugins we need
  required_providers {
    kubernetes = {
      # This plugin lets Terraform talk to Kubernetes
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

# Tell Terraform where our Kubernetes cluster is
# config_path points to the kubeconfig file kubectl uses
# config_context tells it to use our local minikube cluster
provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

# Create a namespace for our app
# Namespace = a isolated space inside Kubernetes for our resources
# Like a folder that keeps our app separate from everything else
resource "kubernetes_namespace" "app" {
  metadata {
    name = var.app_namespace   # uses the variable we defined above
    labels = {
      managed-by  = "terraform"    # marks this as created by terraform
      environment = var.environment
    }
  }
}

# Create a separate namespace for monitoring tools
# Keeping monitoring separate from app is a best practice
resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = "monitoring"
    labels = { managed-by = "terraform" }
  }
}

# ConfigMap = a way to inject configuration into our app
# Instead of hardcoding config inside the app, we store it here
# Kubernetes injects these as environment variables into our containers
resource "kubernetes_config_map" "app_config" {
  metadata {
    name      = "app-config"
    # Place this configmap in the same namespace as our app
    namespace = kubernetes_namespace.app.metadata[0].name
  }
  data = {
    ENV         = var.environment
    APP_VERSION = var.app_version
  }
}

# Outputs print useful information after terraform apply runs
# Like a summary of what was created
output "app_namespace" {
  value = kubernetes_namespace.app.metadata[0].name
}
