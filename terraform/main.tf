resource "azurerm_resource_group" "rg" {
  name     = var.nombre_grupo_recursos
  location = var.localizacion_grupo_recursos
}

resource "azurerm_log_analytics_workspace" "log_analytics" {
  name                = var.nombre_log_analytics
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "apps_environment" {
  name                       = var.nombre_entorno_apps
  location                   = var.localizacion_grupo_recursos
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics.id
  infrastructure_subnet_id   = azurerm_subnet.app_subnet.id

}

resource "azurerm_container_app" "app" {
  name                         = var.nombre_app
  container_app_environment_id = azurerm_container_app_environment.apps_environment.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  template {
    container {
      name   = var.nombre_contenedor
      image  = var.nombre_imagen_contenedor
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name        = "ENTORNO"
        secret_name = "entorno"
      }

      env {
        name        = "POSTGRES_USER"
        secret_name = "user"
      }

      env {
        name        = "POSTGRES_PASSWORD"
        secret_name = "password"
      }

      env {
        name        = "POSTGRES_DB"
        secret_name = "db"
      }

      env {
        name        = "POSTGRES_HOST"
        secret_name = "host"
      }

      env {
        name        = "POSTGRES_PORT"
        secret_name = "port"
      }

    }
  }

  secret {
    name  = "entorno"
    value = var.entorno
  }

  secret {
    name  = "user"
    value = var.user
  }

  secret {
    name  = "password"
    value = var.password
  }

  secret {
    name  = "db"
    value = var.db
  }

  secret {
    name  = "host"
    value = var.host
  }

  secret {
    name  = "port"
    value = var.port
  }

  ingress {
    external_enabled = true
    target_port      = 5000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

resource "azurerm_postgresql_flexible_server" "postgres" {
  name                   = var.postgres
  resource_group_name    = azurerm_resource_group.rg.name
  location               = azurerm_resource_group.rg.location
  administrator_login    = var.user
  administrator_password = var.password

  version                      = "14"
  storage_mb                   = 32768
  sku_name                     = "GP_Standard_D2s_v3"
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false

  authentication {
    active_directory_auth_enabled = false
    password_auth_enabled         = true
  }

  delegated_subnet_id           = azurerm_subnet.postgres_subnet.id
  private_dns_zone_id           = azurerm_private_dns_zone.postgres_dns.id
  zone                          = "1"
  public_network_access_enabled = false

  depends_on = [azurerm_subnet.postgres_subnet]

}

resource "azurerm_postgresql_flexible_server_database" "app_db" {
  name      = var.db
  server_id = azurerm_postgresql_flexible_server.postgres.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_virtual_network" "main" {
  name                = var.vnet
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/22"]
}

resource "azurerm_subnet" "postgres_subnet" {
  name                 = var.postgres_subnet
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]

  delegation {
    name = "postgres_delegation"

    service_delegation {
      name = "Microsoft.DBforPostgreSQL/flexibleServers"
      actions = [
        "Microsoft.Network/virtualNetworks/subnets/join/action"
      ]
    }
  }
}

resource "azurerm_subnet" "app_subnet" {
  name                 = var.container_app_subnet
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/23"]
}

resource "azurerm_private_dns_zone" "postgres_dns" {
  name                = var.postgres_dns
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "postgres_dns_link" {
  name                  = var.postgres_dns_link
  resource_group_name   = azurerm_resource_group.rg.name
  private_dns_zone_name = azurerm_private_dns_zone.postgres_dns.name
  virtual_network_id    = azurerm_virtual_network.main.id
  registration_enabled  = false
}