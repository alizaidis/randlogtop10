resource "google_storage_bucket" "storage_bucket" {
  name                        = var.bucket_name
  project                     = var.project
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
}

resource "google_compute_network" "vpc_network" {
  name = "randlog-vpc"
  project = var.project           
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "vpc-subnet" {
  name          = "subnet"
  ip_cidr_range = "10.2.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc_network.id
  secondary_ip_range {
    range_name    = "subnet-r2"
    ip_cidr_range = "192.168.10.0/24"
  }
}

resource "google_service_account" "randlogcfSA" {
  account_id   = "randlogcfSA"
  display_name = "Service Account"
}

resource "google_service_account" "redisinserterSA" {
  account_id   = "redisinserterSA"
  display_name = "Service Account"
}

resource "google_service_account" "redisgetterSA" {
  account_id   = "redisgetterSA"
  display_name = "Service Account"
}

resource "google_vpc_access_connector" "vpcconnector" {
  name          = "vpcconn"
  region        = var.region
  ip_cidr_range = "10.2.0.0/16"
  network       = var.network
}

module "redis"{
    source      = "../modules/redis"
    name        = "randlogredis"
    authorized_network = data.google_compute_network.vpc_network.name

}

#TODOcloudfunction
#TODOloudfunction
#TODOloudfunction
