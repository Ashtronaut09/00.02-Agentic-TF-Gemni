terraform {

  cloud {
    organization = "Ashs-Test-Enviorment"

    workspaces {
      name = "0002-Agentic-TF-Gemni"
    }
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.31.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.1"
    }
  }

  required_version = ">= 1.2"
}