#!/bin/bash

# Prompt for user inputs
read -p "Enter the path to your Flask application (e.g., /home/user/myapp): " app_path
read -p "Enter your server's domain name (e.g., example.com): " domain_name

# Update package lists
sudo apt-get update

# Install required packages
sudo apt-get install -y python3-pip python3-venv nginx

# Create a new virtual environment
python3 -m venv cv-extractor-env

# Activate the virtual environment
source cv-extractor-env/bin/activate

# Install required Python packages
pip install flask docx PyPDF2 openpyxl

# Deactivate the virtual environment
deactivate

# Create a systemd service file
cat << EOF > /etc/systemd/system/cv-extractor.service
[Unit]
Description=CV Extractor Web Application
After=network.target

[Service]
User=$(whoami)
Group=$(id -gn)
WorkingDirectory=$app_path
EnvironmentFile=$app_path/cv-extractor-env/bin/activate
ExecStart=$app_path/cv-extractor-env/bin/python3 $app_path/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the systemd service
sudo systemctl enable cv-extractor
sudo systemctl start cv-extractor

# Configure Nginx as a reverse proxy
sudo rm /etc/nginx/sites-enabled/default
sudo tee /etc/nginx/sites-available/cv-extractor > /dev/null << EOF
server {
    listen 80;
    server_name $domain_name;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF

# Enable the Nginx configuration
sudo ln -s /etc/nginx/sites-available/cv-extractor /etc/nginx/sites-enabled/
sudo systemctl restart nginx

echo "CV Extractor web application is now running at http://$domain_name"