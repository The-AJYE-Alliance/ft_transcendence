ui = true
api_addr = "https://vault:8200"

storage "file" {
  path = "/vault/data"
}

listener "tcp" {
  address       = "vault:8200"
  tls_cert_file = "/vault/ssl/cert.pem"
  tls_key_file  = "/vault/ssl/key.pem"
  tls_min_version = "tls13"
}