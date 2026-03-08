# ContractorPro - Docker Setup Instructions

Run ContractorPro on your local machine using Docker - no complex installation required!

## Prerequisites

You need Docker installed on your computer:

### Windows:
1. Download **Docker Desktop** from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation: Open PowerShell or Command Prompt and run:
   ```
   docker --version
   ```

### Mac:
1. Download **Docker Desktop** from: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation: Open Terminal and run:
   ```
   docker --version
   ```

### Linux:
1. Install Docker Engine: https://docs.docker.com/engine/install/
2. Verify installation:
   ```
   docker --version
   ```

---

## Quick Start (Easy Method)

### Step 1: Extract the ContractorPro folder
- Unzip the ContractorPro folder to your desired location
- Example: `C:\ContractorPro` or `~/ContractorPro`

### Step 2: Open Terminal/Command Prompt
- **Windows**: Right-click in the ContractorPro folder → "Open in Terminal" or use PowerShell
- **Mac/Linux**: Open Terminal and navigate to the folder:
  ```bash
  cd /path/to/ContractorPro
  ```

### Step 3: Build and Run
Run this single command:
```bash
docker-compose up -d
```

That's it! The app will:
- Build the Docker image
- Start the container
- Initialize the database
- Start running on port 5000

### Step 4: Access the App
Open your browser and go to:
```
http://localhost:5000
```

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

---

## Manual Docker Commands (Alternative Method)

If you don't want to use docker-compose:

### Build the Docker image:
```bash
docker build -t contractorpro .
```

### Run the container:
```bash
docker run -d -p 5000:5000 --name contractorpro-app contractorpro
```

### Access the app:
```
http://localhost:5000
```

---

## Managing the App

### Stop the app:
```bash
docker-compose down
```

### Restart the app:
```bash
docker-compose restart
```

### View logs:
```bash
docker-compose logs -f
```

### Stop and remove everything:
```bash
docker-compose down -v
```

---

## Troubleshooting

### Port 5000 already in use?
Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Use port 8080 instead
```
Then access at: http://localhost:8080

### Can't access the app?
1. Check if Docker is running:
   ```bash
   docker ps
   ```
2. Check container logs:
   ```bash
   docker-compose logs
   ```

### Reset the database:
```bash
docker-compose down -v
docker-compose up -d
```

---

## Sharing Data Between Runs

The app stores data in:
- `contractorpro.db` - SQLite database (all your jobs, quotes, contracts)
- `uploads/` - Photos and documents

These persist even when you stop/restart the container.

---

## System Requirements

- **RAM**: 512MB minimum, 1GB recommended
- **Disk**: 500MB for Docker image + data
- **OS**: Windows 10+, macOS 10.14+, or Linux with Docker support

---

## What's Included

ContractorPro includes:
- Job management system
- Multi-layer POS quote generator with job specifications
- Comprehensive contract generation with editable sections
- Task management and calendar
- Lead tracking
- Estimate builder
- Progress photo tracking
- Analytics and reporting

---

## Support

For issues or questions, refer to the main documentation in the `docs/` folder.

**Quick Links:**
- User Manual: `docs/USER_MANUAL.md`
- API Documentation: `docs/API_DOCUMENTATION.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`
