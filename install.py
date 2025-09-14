#!/usr/bin/env python3
"""
ContractorPro Installation Script
Run this to set up the application for the first time
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install Python packages"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    return run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                      "Installing Python packages")

def setup_database():
    """Initialize the database"""
    return run_command(f"{sys.executable} migrate.py init", 
                      "Setting up database")

def add_sample_data():
    """Add sample data"""
    return run_command(f"{sys.executable} migrate.py seed", 
                      "Adding sample data")

def create_directories():
    """Create necessary directories"""
    directories = ['uploads', 'uploads/photos', 'uploads/documents', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")
    return True

def main():
    print("🏗️  ContractorPro Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Install packages
    if not install_requirements():
        print("❌ Failed to install requirements")
        print("\n💡 Try running manually:")
        print(f"   {sys.executable} -m pip install -r requirements.txt")
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("❌ Failed to setup database")
        print("\n💡 Try running manually:")
        print(f"   {sys.executable} migrate.py init")
        sys.exit(1)
    
    # Add sample data
    print("\n📊 Would you like to add sample data for testing? (y/N): ", end="")
    try:
        response = input().strip().lower()
        if response in ['y', 'yes']:
            if not add_sample_data():
                print("⚠️  Failed to add sample data (optional)")
    except KeyboardInterrupt:
        print("\n⏭️  Skipping sample data")
    
    print("\n" + "=" * 50)
    print("🎉 Installation Complete!")
    print("\n📋 Next Steps:")
    print("1. Run the application:")
    print(f"   {sys.executable} app.py")
    print("\n2. Open your browser to:")
    print("   http://localhost:5000")
    print("\n3. Login with:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n📚 Documentation:")
    print("   - Setup Guide: SETUP.md")
    print("   - Full Docs: docs/README.md")
    print("\n🔧 Configuration:")
    print("   - Edit .env for custom settings")
    print("   - Update email settings for notifications")

if __name__ == '__main__':
    main()