#!/bin/bash
sudo apt-get update
sudo apt-get install -y apache2
echo 'Hello from Terraform' > /var/www/html/index.html
