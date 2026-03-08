# How to Distribute ContractorPro

## 📦 What to Send to People

### Option 1: ZIP File (Simplest)

1. **Zip the entire folder** `Website_Test_Folder`
2. **Send the ZIP file** via email, Google Drive, Dropbox, etc.
3. **Include this message:**

---

**Subject: ContractorPro - Construction Management App**

Hi!

I'm sharing ContractorPro - a containerized construction business management application.

**What's included:**
- Multi-layer POS quote generator
- Job and contract management
- Task scheduling and calendar
- Lead tracking and estimates
- Progress photo documentation

**To run it:**

1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop (free)
2. **Extract the ZIP** to any folder
3. **Open Terminal/Command Prompt** in that folder
4. **Run**: `docker-compose up -d`
5. **Open**: http://localhost:5000 in your browser

**Login:**
- Username: `admin`
- Password: `admin123`

**See `README_DOCKER.md` for quick start or `DOCKER_SETUP.md` for detailed instructions.**

---

### Option 2: GitHub Repository (If you use Git)

1. Create a GitHub repository
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/contractorpro.git
   git push -u origin main
   ```
3. Share the GitHub URL
4. They clone and run:
   ```bash
   git clone https://github.com/yourusername/contractorpro.git
   cd contractorpro
   docker-compose up -d
   ```

### Option 3: Docker Hub (Public Docker Image)

**Advanced:** Build and push to Docker Hub so people can run without downloading the code:

```bash
docker build -t yourusername/contractorpro:latest .
docker push yourusername/contractorpro:latest
```

Then they just run:
```bash
docker run -d -p 5000:5000 yourusername/contractorpro:latest
```

---

## 🔒 Security Notes

**Before Distribution:**

1. **Change the default password** in the database or create new users
2. **Remove sensitive data** from the database:
   ```bash
   python migrate.py reset
   python migrate.py init
   ```
3. **Check `.env` file** - make sure no API keys or secrets are included
4. **Review `contractorpro.db`** - delete if it contains real data

**Optional: Add authentication**
- Consider adding a strong admin password
- Create multiple user accounts for recipients

---

## 📊 What People Get

When they run your Docker container, they get:
- Complete working app on their local machine
- No internet required (runs offline)
- Their own private database
- Full access to all features
- No data shared with you or anyone else

---

## 💾 File Size

The distribution package:
- **Source code**: ~5-10 MB
- **Docker image** (when built): ~200-300 MB
- **Total download size** (ZIP): ~5-10 MB
- **Required disk space** (including Docker): ~500 MB

---

## 🎯 Recommended Distribution Method

**For non-technical users:** ZIP file + clear instructions (Option 1)

**For developers:** GitHub repository (Option 2)

**For production deployment:** Docker Hub image (Option 3)

---

## 📝 Files to Include

**Required:**
- All Python files (`*.py`)
- `templates/` folder
- `static/` folder
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `README_DOCKER.md`
- `.env` file (remove secrets first!)

**Optional but recommended:**
- `DOCKER_SETUP.md`
- `docs/` folder
- `contract_template.txt`

**Exclude:**
- `__pycache__/` folders
- `.git/` folder (unless using GitHub)
- `contractorpro.db` (if it has real data)
- `uploads/` folder (if it has real documents/photos)
- Your personal API keys

---

## 🧪 Before Sending

Test it yourself:
1. Create a fresh folder
2. Copy all files there
3. Run `docker-compose up -d`
4. Verify it works at http://localhost:5000
5. Test the quote generator and contract features
6. Then ZIP and send

---

**Your app is now portable, secure, and easy to distribute!**
