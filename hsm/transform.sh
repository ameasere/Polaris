#!/bin/bash

# Color codes for printing
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Function to print in green color
print_success() {
  echo -e "${GREEN}$1${NC}"
}

# Function to print in red color
print_error() {
  echo -e "${RED}$1${NC}"
}

print_blue() {
  echo -e "${BLUE}$1${NC}"
}

print_magenta() {
  echo -e "${MAGENTA}$1${NC}"
}

print_yellow() {
  echo -e "${YELLOW}$1${NC}"
}

loading_icon() {
  echo -n "Initializing "
  for _ in {1..3}; do
    echo -n "."
    sleep 1
  done
  echo
}

print_banner() {
  print_magenta "    ____          __              _      "
  print_magenta "   / __ \ ____   / /____ _ _____ (_)_____"
  print_magenta "  / /_/ // __ \ / // __ \`// ___// // ___/"
  print_magenta " / ____// /_/ // // /_/ // /   / /(__  ) "
  print_magenta "/_/     \____//_/ \__,_//_/   /_//____/  "
  echo -e "\n"
}

# Function to print terms and conditions
print_terms() {
  clear
  printf "%*s\n" $(( ($(tput cols) + 24) / 2)) "Terms and Conditions"
  # Print number of dashes depending on the terminal width
  # shellcheck disable=SC2183
  printf "%*s\n" $(( ($(tput cols) + 24) / 2)) | tr " " "-"
  print_blue "1. Any damage or loss of data as a result of Polaris is not the responsibility of Ameasere. \nAmeasere cannot guarantee that all devices are compatible and stable with Polaris. \n\033[0;31mIf you have any doubt, thoroughly examine the code on our GitHub first."
  print_magenta "► CTRL + Click to open the GitHub link: https://github.com/ameasere/polaris"
  echo -e "\n"
  print_blue "2. Polaris was developed as a contribution towards advancing cryptographical standards and accessibility. \nIn no way does Ameasere endorse nor encourage using Polaris for a nefarious purpose."
  print_magenta "► Using the Polaris API and server-side infrastructure for malicious purposes will result in your account being terminated and legal action being filed."
  echo -e "\n"
  print_blue "3. Your third term here."
  # Add more terms as needed
  # shellcheck disable=SC2183
  printf "%*s\n" $(( ($(tput cols) + 24) / 2)) | tr " " "-"
  printf "%*s\n" $(( ($(tput cols) + 28) / 2)) "[Y] Agree and Continue    [N] Reject and Terminate"
}
print_banner
loading_icon
print_terms
trap '' SIGINT
read -r -p "[Y/N]: " terms

check_pre_reqs() {
  # Check if running as root. If not, prompt for sudo password
  if [ "$EUID" -ne 0 ]; then
    print_yellow "This script needs to be run as root."
    print_yellow "Please enter your sudo password to continue..."
    sudo echo -n
  fi

  # Check if the user has installed the required dependencies
  # OpenSSL, libssl-dev, python3, python3-pip, python3-venv

  print_yellow "Checking if you have the required dependencies installed..."
  sleep 1

  # Function to check if a package is installed
  is_package_installed() {
    if command -v "$1" &>/dev/null; then
      return 0 # Package is installed
    else
      return 1 # Package is not installed
    fi
  }

  # Check dependencies based on the distribution
  if is_package_installed "pacman"; then
    # Arch Linux
    # Run the install command, if it is installed already then DO NOT reinstall
    sudo pacman -S "openssl" "python3" "unzip" "ufw" "jq" --noconfirm --needed
  elif is_package_installed "apt"; then
    # Debian and Ubuntu
    # Run the install command, if it is installed already then it will skip it
    sudo apt install openssl python3 python3-pip python3-venv unzip ufw jq -y
  elif is_package_installed "dnf"; then
    # Fedora
    # Run the install command, if it is installed already then it will skip it
    sudo dnf install openssl python3 python3-pip python3-venv unzip ufw jq -y
  else
    print_error "Error: Unsupported distribution. Please install the required dependencies manually."
    exit 1
  fi

  print_success "All required dependencies are installed."
}

install_pip_packages() {
  # Install the required pip packages
  print_yellow "Installing the required pip packages..."
  sleep 1
  pip3 install --upgrade pip
  pip3 install --upgrade cryptography psutil pycryptodome twofish rsa
  print_success "All required pip packages are installed."
}

download_polaris_driver() {
  # First, ensure a request to ameasere.com resolves to the correct IP address
  print_yellow "Checking if ameasere.com resolves to the correct IP address..."
  print_magenta "! Ensure your DNS is not poisoned or hijacked, and that any hosts file is not modified. !"
  sleep 3
  ip_address=$(ping -c 3 ameasere.com | grep -oP "\d+\.\d+\.\d+\.\d+" | head -1)
  ips_from_dns=$(dig +short ameasere.com | head -2)
  first_ip=$(echo "$ips_from_dns" | head -1)
  second_ip=$(echo "$ips_from_dns" | tail -1)
  if [ "$ip_address" == "$first_ip" ] || [ "$ip_address" == "$second_ip" ]; then
    print_success "ameasere.com resolves to the correct IP address."
  else
    print_error "ameasere.com does not resolve to the correct IP address."
    print_yellow "Are you sure you want to continue? [Y/N]"
    read -r -p "[Y/N]: " ip_address_check
    if [ "$ip_address_check" == "Y" ] || [ "$ip_address_check" == "y" ]; then
      print_success "You have agreed to continue. Continuing..."
      sleep 1
    elif [ "$ip_address_check" == "N" ] || [ "$ip_address_check" == "n" ]; then
      print_error "You have rejected to continue. Configuration of the HSM will not continue."
      exit 1
    else
      print_error "Invalid input. Please try again."
      exit 1
    fi
  fi
  # Download the Polaris driver
  print_yellow "Downloading the Polaris driver..."
  # Check if this is an ARM64 machine or x86_64
  if [ "$(uname -m)" == "aarch64" ]; then
    # ARM64
    wget -q https://cdn.ameasere.com/polaris/driver-arm64.zip -O driver-arm64.zip
    unzip -q driver-arm64.zip -d polaris_driver
    rm driver-arm64.zip
  else
    # x86_64
    wget -q https://cdn.ameasere.com/polaris/driver-x86.zip -O driver-x86.zip
    unzip -q driver-x86.zip -d polaris_driver
    rm driver-x86.zip
  fi
  sleep 1
  print_success "Polaris driver downloaded successfully."
}

check_driver_sum() {
  # Check the SHA256 sum of the driver
  print_yellow "Checking the SHA256 sum of the driver..."
  sleep 1
  # Get the SHA256 sum of the driver
  if [ "$(uname -m)" == "aarch64" ]; then
    driver_sum=$(sha256sum polaris_driver/driver.bin | awk '{print $1}')
    wget -q https://cdn.ameasere.com/polaris/driver-arm64.sha256 -O driver.sha256
  else
    driver_sum=$(sha256sum polaris_driver/driver.bin | awk '{print $1}')
    wget -q https://cdn.ameasere.com/polaris/driver-x86.sha256 -O driver.sha256
  fi
  server_sum=$(cat driver.sha256)
  if [ "$driver_sum" == "$server_sum" ]; then
    print_success "SHA256 sum of the driver matches the one on the server."
  else
    print_error "SHA256 sum of the driver does not match the one on the server."
    print_yellow "Are you sure you want to continue? [Y/N]"
    read -r -p "[Y/N]: " driver_sum_check
    if [ "$driver_sum_check" == "Y" ] || [ "$driver_sum_check" == "y" ]; then
      print_success "You have agreed to continue. Continuing..."
      sleep 1
    elif [ "$driver_sum_check" == "N" ] || [ "$driver_sum_check" == "n" ]; then
      print_error "You have rejected to continue. Configuration of the HSM will not continue."
      exit 1
    else
      print_error "Invalid input. Please try again."
      exit 1
    fi
  fi
}

configure_system() {
  # Check if ASLR is enabled
  print_yellow "Checking if ASLR is enabled..."
  sleep 1
  if [ "$(cat /proc/sys/kernel/randomize_va_space)" == "2" ]; then
    print_success "ASLR is enabled."
  else
    print_error "ASLR is not enabled. Enabling it..."
    sudo sysctl -w kernel.randomize_va_space=2
    # Write the setting to the sysctl.conf file if it exists, or /etc/sysctl.d/10-polaris.conf if it doesn't
    if [ -f /etc/sysctl.conf ]; then
      sudo sed -i 's/kernel.randomize_va_space=0/kernel.randomize_va_space=2/g' /etc/sysctl.conf
    else
      sudo echo "kernel.randomize_va_space=2" | sudo tee /etc/sysctl.d/10-polaris.conf
    fi
    print_success "ASLR enabled successfully. This will require a reboot to take effect."
  fi
  # If log file exists, delete it and create a new one
  if [ -f /var/log/polaris.log ]; then
    sudo rm /var/log/polaris.log
    sudo touch /var/log/polaris.log
  else
    sudo touch /var/log/polaris.log
  fi
    chown root:root /var/log/polaris.log
    chmod 640 /var/log/polaris.log
    systemctl restart rsyslog
  # Generate the salt for the machine, saving it in file: /etc/polaris/salt
  print_yellow "Generating the salt for the machine..."
  sleep 1
  # curl -s https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971/public/latest | jq -r '.randomness' | head -c 32 | sudo tee /etc/polaris/salt
  # DO NOT PRINT THIS TO CONSOLE
  if [ -d /etc/polaris ]; then
  print_yellow "The /etc/polaris directory already exists. Do you want to keep or replace it? [K/R]"
  read -r -p "[K/R]: " keep_replace
    if [ "$keep_replace" == "K" ] || [ "$keep_replace" == "k" ]; then
      print_success "You have chosen to keep the /etc/polaris directory."
      sleep 1
    elif [ "$keep_replace" == "R" ] || [ "$keep_replace" == "r" ]; then
      print_yellow "You have chosen to replace the /etc/polaris directory. Continuing..."
      sleep 1
      sudo rm -rf /etc/polaris
      sudo mkdir -p /etc/polaris
    else
      print_error "Invalid input. Please try again."
      exit 1
    fi
  else
    sudo mkdir -p /etc/polaris
  fi
  curl -s https://api.drand.sh/52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971/public/latest | jq -r '.randomness' | head -c 32 | sudo tee /etc/polaris/salt > /dev/null
  chmod 640 /etc/polaris/salt
  chown root:root /etc/polaris/salt
  print_success "Salt generated successfully."
  # If /etc/polaris directory exists, the user should choose to keep or replace it

  # Add firewall rule to allow incoming connections on port 26555
  print_yellow "Adding firewall rule to allow incoming connections on port 26555..."
  sleep 1
  sudo ufw allow 26555/tcp
  sudo ufw allow 26556/tcp
  #sudo ufw deny 22/tcp // Disable this for testing purposes only, so you don't get locked out!
  sudo ufw --force enable
  print_success "Firewall rule added successfully."
  # chmod and chown the driver to 700 and root:root
  sudo chmod 700 polaris_driver/driver.bin
  sudo chown root:root polaris_driver/driver.bin
  # Make the driver start on boot
  print_yellow "Making the driver start on boot..."
  sleep 1
  sudo cp polaris_driver/driver.bin /usr/local/bin/polaris_driver
  sudo cp polaris_driver/polaris_driver.service /etc/systemd/system/polaris_driver.service
  sudo systemctl daemon-reload
  sudo systemctl enable polaris_driver.service
  print_success "Polaris driver will start on boot."
  # Start the driver
  print_yellow "Starting the driver..."
  sleep 1
  sudo systemctl start polaris_driver.service
  print_success "Polaris driver started successfully."
  # Check if the driver is running
  print_yellow "Checking if the driver is running..."
  sleep 1
  if systemctl is-active --quiet polaris_driver.service; then
    print_success "Polaris driver is running."
  else
    print_error "Polaris driver is not running."
    print_yellow "Are you sure you want to continue? [Y/N]"
    read -r -p "[Y/N]: " driver_running_check
    if [ "$driver_running_check" == "Y" ] || [ "$driver_running_check" == "y" ]; then
      print_success "You have agreed to continue. Continuing..."
      sleep 1
    elif [ "$driver_running_check" == "N" ] || [ "$driver_running_check" == "n" ]; then
      print_error "You have rejected to continue. Configuration of the HSM will not continue."
      exit 1
    else
      print_error "Invalid input. Please try again."
      exit 1
    fi
  fi
}

if [ "$terms" == "Y" ] || [ "$terms" == "y" ]; then
  print_success "You have agreed to the terms and conditions. Continuing..."
  sleep 1
  # Clear the screen and continue with the script
  clear
  print_blue "Starting the configuration of the HSM..."
  check_pre_reqs
  install_pip_packages
  download_polaris_driver
  check_driver_sum
  configure_system
  print_success "Configuration of the HSM is complete."
elif [ "$terms" == "N" ] || [ "$terms" == "n" ]; then
  print_error "You have rejected the terms and conditions. Configuration of the HSM will not continue."
  exit 1
else
  print_error "Invalid input. Please try again."
  exit 1
fi
