# AiFunCheckApp1 Troubleshooting Guide

## Quick Start

### Prerequisites
1. AWS credentials configured (run `source .aws-creds.sh` if available)
2. Python 3 installed
3. Access to the Lightsail instance

### Running the Diagnostic Script

```bash
# Navigate to the troubleshooting tools directory
cd troubleshooting-tools-nodejs

# Run the diagnostic script
python3 debug-aifuncheckapp1.py

# When prompted:
Instance name [AiFunCheckApp1]: AiFunCheckApp1
AWS region [us-east-1]: us-east-1
```

## What the Script Checks

The diagnostic script performs a comprehensive check of:

1. **Node.js & npm Installation** - Verifies Node.js, npm, and npx are installed
2. **TypeScript Installation** - Checks if TypeScript compiler is available
3. **Application Directory** - Validates directory structure and key files
4. **Package.json Configuration** - Reviews entry points and scripts
5. **PM2 Process Manager** - Checks if PM2 is running the application
6. **PM2 Logs** - Displays recent application logs
7. **Ecosystem Configuration** - Validates PM2 configuration file
8. **Port 3000 Status** - Verifies if the application is listening
9. **Node.js Processes** - Lists all running Node.js processes
10. **Health Endpoint** - Tests `/api/health` endpoint locally
11. **Environment Variables** - Checks for .env file
12. **System Logs** - Reviews recent system logs for errors
13. **Disk Space** - Checks available disk space
14. **Memory Usage** - Reviews memory consumption
15. **Deployment Activity** - Shows recent git commits

## Common Issues and Solutions

### Issue 1: TypeScript Not Compiled (dist folder missing)

**Symptom:**
```
❌ dist directory NOT found (TypeScript not compiled)
```

**Solution:**
```bash
# SSH into the instance
ssh ubuntu@<instance-ip>

# Navigate to app directory
cd /var/www/aifuncheckapp1

# Install dependencies if needed
npm install

# Build TypeScript
npm run build

# Verify dist folder was created
ls -la dist/

# Restart PM2
pm2 restart aifuncheckapp1
```

### Issue 2: Application Not Listening on Port 3000

**Symptom:**
```
❌ No process listening on port 3000
```

**Solution:**
```bash
# Check PM2 status
pm2 status

# View PM2 logs
pm2 logs aifuncheckapp1 --lines 50

# If process is not running, start it
pm2 start ecosystem.config.js

# If process is errored, restart it
pm2 restart aifuncheckapp1

# Save PM2 process list
pm2 save
```

### Issue 3: Health Endpoint Not Responding

**Symptom:**
```
❌ Failed to connect to health endpoint
```

**Possible Causes:**
1. Application not started
2. Wrong entry point in PM2
3. Port conflict
4. Application crashed

**Solution:**
```bash
# Check if dist/index.js exists
ls -la /var/www/aifuncheckapp1/dist/index.js

# Check PM2 logs for errors
pm2 logs aifuncheckapp1 --lines 100

# Verify ecosystem.config.js points to correct file
cat /var/www/aifuncheckapp1/ecosystem.config.js

# Test starting manually
cd /var/www/aifuncheckapp1
node dist/index.js

# If it works, restart PM2
pm2 restart aifuncheckapp1
```

### Issue 4: PM2 Not Installed

**Symptom:**
```
❌ PM2 NOT installed
```

**Solution:**
```bash
# Install PM2 globally
sudo npm install -g pm2

# Start the application
cd /var/www/aifuncheckapp1
pm2 start ecosystem.config.js

# Configure PM2 to start on boot
pm2 startup
pm2 save
```

### Issue 5: Node Modules Missing

**Symptom:**
```
❌ node_modules directory NOT found
```

**Solution:**
```bash
cd /var/www/aifuncheckapp1
npm install
npm run build
pm2 restart aifuncheckapp1
```

## Manual Verification Steps

After running the diagnostic script, you can manually verify:

```bash
# 1. Check Node.js version
node --version

# 2. Check npm version
npm --version

# 3. Check if TypeScript is compiled
ls -la /var/www/aifuncheckapp1/dist/

# 4. Check PM2 status
pm2 status

# 5. View PM2 logs
pm2 logs aifuncheckapp1

# 6. Test health endpoint locally
curl http://localhost:3000/api/health

# 7. Test health endpoint externally
curl http://<instance-ip>/api/health

# 8. Check what's listening on port 3000
sudo netstat -tlnp | grep :3000

# 9. Check PM2 ecosystem config
cat /var/www/aifuncheckapp1/ecosystem.config.js

# 10. Check package.json scripts
cat /var/www/aifuncheckapp1/package.json | grep -A 10 scripts
```

## Deployment Workflow

The expected deployment workflow is:

1. **Code Push** → GitHub repository
2. **GitHub Actions** → Runs tests and builds
3. **Deploy to Lightsail** → Transfers files to instance
4. **Install Dependencies** → `npm install`
5. **Build TypeScript** → `npm run build` (creates dist folder)
6. **Start with PM2** → `pm2 start ecosystem.config.js`
7. **Health Check** → Verifies `/api/health` endpoint

## Expected File Structure

```
/var/www/aifuncheckapp1/
├── dist/                    # Compiled TypeScript (created by npm run build)
│   ├── index.js            # Main entry point
│   ├── api/
│   ├── models/
│   ├── services/
│   └── storage/
├── src/                     # TypeScript source files
│   ├── index.ts
│   ├── api/
│   ├── models/
│   ├── services/
│   └── storage/
├── node_modules/            # Dependencies
├── package.json             # Node.js configuration
├── tsconfig.json            # TypeScript configuration
├── ecosystem.config.js      # PM2 configuration
└── .env                     # Environment variables (optional)
```

## Interpreting the Diagnostic Output

### ✅ Green Checkmarks
Indicates the component is working correctly.

### ❌ Red X Marks
Indicates a problem that needs attention.

### ⚠️  Yellow Warnings
Indicates something that might be an issue but isn't critical.

## Getting Help

If the diagnostic script doesn't resolve your issue:

1. **Review the full output** - Look for error messages in PM2 logs
2. **Check GitHub Actions logs** - Verify the deployment completed successfully
3. **Review system logs** - Check `/var/log/syslog` for system-level errors
4. **Test locally** - Try running the application manually with `node dist/index.js`

## Integration with GitHub Actions

This diagnostic script is designed to work with the automated deployment workflow. If deployment fails:

1. Check GitHub Actions logs first
2. Run this diagnostic script to identify server-side issues
3. Apply fixes based on the recommendations
4. Re-run the deployment if needed

## Additional Resources

- [Node.js Documentation](https://nodejs.org/docs/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [PM2 Documentation](https://pm2.keymetrics.io/docs/)
- [Express.js Guide](https://expressjs.com/)
