#!/usr/bin/env python3
import os
import subprocess
import getpass


def get_user_input():
    """Prompt user for required information"""
    dir_name = input("Enter directory name: ").strip()
    remote_dir = input("Enter remote directory name: ").strip()
    ssh_host = input("Enter SSH host name: ").strip()
    domain_name = input("Enter domain name: ").strip()
    return dir_name, remote_dir, ssh_host, domain_name


def create_makefile(dir_name, remote_dir, ssh_host):
    """Create Makefile with specified format"""
    makefile_content = f"""copy:
\trsnc -av --exclude-from='.gitignore' ./ {ssh_host}:/{remote_dir}

sync:
\trsnc -av --exclude-from='.gitignore' ./ {ssh_host}:/{remote_dir}; ssh {ssh_host} cd /{remote_dir} && rm uv.lock && uv sync; ssh {ssh_host} systemctl restart {dir_name}.service; ssh {ssh_host} journalctl -u {dir_name}.service -n 100 -f

stop:
\tssh {ssh_host} systemctl stop {dir_name}.service;

start:
\tssh {ssh_host} systemctl start {dir_name}.service;

log:
\tssh {ssh_host} journalctl -u {dir_name}.service -n 1000 -f
"""
    with open("Makefile", "w") as f:
        f.write(makefile_content)
    print("Makefile created successfully")


def create_nginx_config(ssh_host, dir_name, domain_name, remote_dir):
    """Create and deploy NGINX configuration"""
    nginx_config = f"""server {{
    listen 80;
    server_name {domain_name};

    root /{remote_dir};
    index index.html index.htm;

    location / {{
        try_files $uri $uri/ /index.html;
    }}
}}
"""
    # Write temp config file
    with open("nginx_temp.conf", "w") as f:
        f.write(nginx_config)

    # Copy to server and move to sites-available
    try:
        subprocess.run(
            f"scp nginx_temp.conf {ssh_host}:/tmp/{dir_name}.conf",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"ssh {ssh_host} 'sudo mv /tmp/{dir_name}.conf /etc/nginx/sites-available/{dir_name}'",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"ssh {ssh_host} 'sudo ln -sf /etc/nginx/sites-available/{dir_name} /etc/nginx/sites-enabled/'",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"ssh {ssh_host} 'sudo nginx -t && sudo systemctl reload nginx'",
            shell=True,
            check=True,
        )
        print("NGINX configuration created and enabled")
    finally:
        os.remove("nginx_temp.conf")


def create_systemd_service(ssh_host, dir_name, remote_dir):
    """Create and deploy systemd service file"""
    service_content = f"""[Unit]
Description={dir_name} service
After=network.target

[Service]
Type=simple
WorkingDirectory=/{remote_dir}
ExecStart=/usr/bin/uv run main.py
Restart=always
User=www-data
Group=www-data

[Install]
WantedBy=multi-user.target
"""
    # Write temp service file
    with open("service_temp.service", "w") as f:
        f.write(service_content)

    # Copy to server and enable
    try:
        subprocess.run(
            f"scp service_temp.service {ssh_host}:/tmp/{dir_name}.service",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"ssh {ssh_host} 'sudo mv /tmp/{dir_name}.service /etc/systemd/system/{dir_name}.service'",
            shell=True,
            check=True,
        )
        subprocess.run(
            f"ssh {ssh_host} 'sudo systemctl daemon-reload'", shell=True, check=True
        )
        subprocess.run(
            f"ssh {ssh_host} 'sudo systemctl enable {dir_name}.service'",
            shell=True,
            check=True,
        )
        print("Systemd service created and enabled")
    finally:
        os.remove("service_temp.service")


def main():
    try:
        # Get user input
        dir_name, remote_dir, ssh_host, domain_name = get_user_input()

        # Create Makefile
        create_makefile(dir_name, remote_dir, ssh_host)

        # Create and deploy NGINX config
        create_nginx_config(ssh_host, dir_name, domain_name, remote_dir)

        # Create and deploy systemd service
        create_systemd_service(ssh_host, dir_name, remote_dir)

        print("Setup completed successfully!")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
