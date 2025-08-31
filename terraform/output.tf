output "container_app_url" {
  value       = azurerm_container_app.app.latest_revision_fqdn
  description = "URL del Container App"
}

output "postgres_flexible_server_fqdn" {
  value       = azurerm_postgresql_flexible_server.postgres.fqdn
  description = "FQDN del servidor PostgreSQL Flexible Server (puerto 5432 por defecto)"
}