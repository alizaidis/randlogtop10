resource "google_project_service" "service" {
  for_each = toset([
    "cloudapis.googleapis.com",
    "cloudbilling.googleapis.com",
    "cloudbuild.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "compute.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "pubsub.googleapis.com",
    "servicemanagement.googleapis.com",
    "serviceusage.googleapis.com",
    "storage-api.googleapis.com",
    "storage-component.googleapis.com",
    "storage.googleapis.com",
    "redis.googleapis.com"
  ])

  service = each.key

  project            = var.project
  disable_on_destroy = true
}



