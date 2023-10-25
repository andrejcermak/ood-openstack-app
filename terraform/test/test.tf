variable "token" {
  type = string
}

terraform {
  required_providers {
    openstack = {
      source = "terraform-provider-openstack/openstack"
    }
  }
  required_version = ">= 0.13"
}

provider "openstack" {
	token = var.token
	auth_url    = "https://identity.ostrava.openstack.cloud.e-infra.cz/v3"
	region      = "Ostrava"
	allow_reauth = false
}

# Create the VM instance
resource "openstack_compute_instance_v2" "example_instance" {
  name            = "example-instance"
  flavor_name     = "m1.small"

  image_name = "ubuntu-focal-x86_64"
}
