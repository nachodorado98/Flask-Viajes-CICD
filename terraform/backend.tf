terraform {
  backend "azurerm" {
    resource_group_name  = "rg-backend-nacho"
    storage_account_name = "tfstatenacho123"
    container_name       = "tfstateviajes"
    key                  = "terraformnachoviajes.tfstate"
  }
}