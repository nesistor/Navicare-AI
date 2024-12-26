output "api_url" {
  value = google_cloud_run_service.api_service.status[0].url
}

output "web_url" {
  value = google_cloud_run_service.web_service.status[0].url
}
