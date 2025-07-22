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
      version = "~> 5.0"
    }
  }

  required_version = ">= 1.2"
}