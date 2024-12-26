resource "google_project_iam_binding" "artifact_registry_permissions" {
  project = var.project_id

  role    = "roles/artifactregistry.writer"
  members = ["serviceAccount:${google_cloud_run_service.api_service.service_account_email}",
             "serviceAccount:${google_cloud_run_service.web_service.service_account_email}"]
}

resource "google_project_iam_binding" "cloud_run_permissions" {
  project = var.project_id

  role    = "roles/run.admin"
  members = ["serviceAccount:${google_cloud_run_service.api_service.service_account_email}",
             "serviceAccount:${google_cloud_run_service.web_service.service_account_email}"]
}