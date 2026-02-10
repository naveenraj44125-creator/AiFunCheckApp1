#!/usr/bin/env python3
"""
Comprehensive diagnostic script for AiFunCheckApp1 Node.js deployment
Checks Node.js, npm, PM2, TypeScript build, and application status
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from workflows.lightsail_common import LightsailBase

def main():
    instance_name = input("Instance name [AiFunCheckApp1]: ").strip() or 'AiFunCheckApp1'
    region = input("AWS region [us-east-1]: ").strip() or 'us-east-1'
    
    print("\n🔍 Debugging AiFunCheckApp1 Node.js Deployment")
    print("=" * 80)
    
    client = LightsailBase(instance_name, region)
    
    # Get instance IP
    try:
        instance_info = client.lightsail.get_instance(instanceName=instance_name)
        ip_address = instance_info['instance']['publicIpAddress']
        print(f"📍 Instance IP: {ip_address}")
    except Exception as e:
        print(f"❌ Could not get instance IP: {e}")
        return 1
    
    debug_script = '''
echo "================================================================================"
echo "🔍 AiFunCheckApp1 Deployment Diagnostic Report"
echo "================================================================================"
echo ""

# 1. Check Node.js and npm
echo "📋 1. Node.js and npm Installation"
echo "-----------------------------------"
if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js installed: $(node --version)"
else
    echo "❌ Node.js NOT installed"
fi

if command -v npm >/dev/null 2>&1; then
    echo "✅ npm installed: $(npm --version)"
else
    echo "❌ npm NOT installed"
fi

if command -v npx >/dev/null 2>&1; then
    echo "✅ npx available: $(npx --version)"
else
    echo "❌ npx NOT available"
fi

echo ""

# 2. Check TypeScript
echo "📋 2. TypeScript Installation"
echo "-----------------------------------"
if command -v tsc >/dev/null 2>&1; then
    echo "✅ TypeScript installed globally: $(tsc --version)"
else
    echo "⚠️  TypeScript not installed globally (may be in node_modules)"
fi

echo ""

# 3. Check application directory
echo "📋 3. Application Directory Structure"
echo "-----------------------------------"
APP_DIR="/var/www/aifuncheckapp1"
if [ -d "$APP_DIR" ]; then
    echo "✅ Application directory exists: $APP_DIR"
    echo ""
    echo "Directory contents:"
    ls -lah "$APP_DIR" | head -20
    echo ""
    
    # Check for key files
    if [ -f "$APP_DIR/package.json" ]; then
        echo "✅ package.json exists"
    else
        echo "❌ package.json NOT found"
    fi
    
    if [ -f "$APP_DIR/tsconfig.json" ]; then
        echo "✅ tsconfig.json exists"
    else
        echo "❌ tsconfig.json NOT found"
    fi
    
    if [ -d "$APP_DIR/src" ]; then
        echo "✅ src directory exists"
    else
        echo "❌ src directory NOT found"
    fi
    
    if [ -d "$APP_DIR/node_modules" ]; then
        echo "✅ node_modules directory exists"
    else
        echo "❌ node_modules directory NOT found"
    fi
    
    if [ -d "$APP_DIR/dist" ]; then
        echo "✅ dist directory exists (TypeScript compiled)"
        echo ""
        echo "dist contents:"
        ls -lah "$APP_DIR/dist" | head -10
    else
        echo "❌ dist directory NOT found (TypeScript not compiled)"
    fi
else
    echo "❌ Application directory NOT found: $APP_DIR"
fi

echo ""

# 4. Check package.json configuration
echo "📋 4. Package.json Configuration"
echo "-----------------------------------"
if [ -f "$APP_DIR/package.json" ]; then
    echo "Main entry point:"
    grep '"main"' "$APP_DIR/package.json" || echo "No main field found"
    echo ""
    echo "Scripts:"
    grep -A 10 '"scripts"' "$APP_DIR/package.json" | head -15
    echo ""
    echo "Dependencies:"
    grep -A 20 '"dependencies"' "$APP_DIR/package.json" | head -25
fi

echo ""

# 5. Check PM2 status
echo "📋 5. PM2 Process Manager Status"
echo "-----------------------------------"
if command -v pm2 >/dev/null 2>&1; then
    echo "✅ PM2 installed: $(pm2 --version)"
    echo ""
    echo "PM2 Process List:"
    pm2 list
    echo ""
    echo "PM2 Detailed Info:"
    pm2 show aifuncheckapp1 2>/dev/null || echo "No process named 'aifuncheckapp1' found"
else
    echo "❌ PM2 NOT installed"
fi

echo ""

# 6. Check PM2 logs
echo "📋 6. PM2 Application Logs (Last 50 lines)"
echo "-----------------------------------"
if command -v pm2 >/dev/null 2>&1; then
    pm2 logs aifuncheckapp1 --lines 50 --nostream 2>/dev/null || pm2 logs --lines 50 --nostream
else
    echo "PM2 not available"
fi

echo ""

# 7. Check ecosystem config
echo "📋 7. PM2 Ecosystem Configuration"
echo "-----------------------------------"
if [ -f "$APP_DIR/ecosystem.config.js" ]; then
    echo "✅ ecosystem.config.js exists"
    echo ""
    cat "$APP_DIR/ecosystem.config.js"
else
    echo "❌ ecosystem.config.js NOT found"
fi

echo ""

# 8. Check port 3000
echo "📋 8. Port 3000 Status"
echo "-----------------------------------"
if command -v netstat >/dev/null 2>&1; then
    echo "Processes listening on port 3000:"
    sudo netstat -tlnp | grep :3000 || echo "❌ No process listening on port 3000"
elif command -v ss >/dev/null 2>&1; then
    echo "Processes listening on port 3000:"
    sudo ss -tlnp | grep :3000 || echo "❌ No process listening on port 3000"
else
    echo "⚠️  netstat/ss not available"
fi

echo ""

# 9. Check Node.js processes
echo "📋 9. Node.js Processes"
echo "-----------------------------------"
ps aux | grep node | grep -v grep || echo "No Node.js processes running"

echo ""

# 10. Test health endpoint locally
echo "📋 10. Local Health Check"
echo "-----------------------------------"
echo "Testing http://localhost:3000/api/health"
curl -v http://localhost:3000/api/health 2>&1 || echo "❌ Failed to connect to health endpoint"

echo ""

# 11. Check environment variables
echo "📋 11. Environment Variables"
echo "-----------------------------------"
if [ -f "$APP_DIR/.env" ]; then
    echo "✅ .env file exists"
    echo "Environment variables (values hidden):"
    grep -v "^#" "$APP_DIR/.env" | grep -v "^$" | cut -d= -f1
else
    echo "⚠️  .env file NOT found (may not be required)"
fi

echo ""

# 12. Check system logs
echo "📋 12. System Logs (Last 20 lines)"
echo "-----------------------------------"
if [ -f "/var/log/syslog" ]; then
    echo "Recent syslog entries related to Node.js/PM2:"
    sudo tail -20 /var/log/syslog | grep -i "node\|pm2\|error" || echo "No relevant entries"
fi

echo ""

# 13. Check disk space
echo "📋 13. Disk Space"
echo "-----------------------------------"
df -h | grep -E "Filesystem|/$"

echo ""

# 14. Check memory usage
echo "📋 14. Memory Usage"
echo "-----------------------------------"
free -h

echo ""

# 15. Check recent deployments
echo "📋 15. Recent Deployment Activity"
echo "-----------------------------------"
if [ -d "$APP_DIR/.git" ]; then
    echo "Git repository detected"
    echo "Last commit:"
    cd "$APP_DIR" && git log -1 --oneline 2>/dev/null || echo "Could not read git log"
else
    echo "Not a git repository"
fi

echo ""
echo "================================================================================"
echo "✅ Diagnostic Complete"
echo "================================================================================"
'''
    
    print("\n🚀 Running comprehensive diagnostic...")
    success, output = client.run_command(debug_script, timeout=180)
    print(output)
    
    if not success:
        print("\n❌ Debug script failed to execute")
        return 1
    
    # Analyze output and provide recommendations
    print("\n" + "="*80)
    print("📊 ANALYSIS & RECOMMENDATIONS")
    print("="*80)
    
    issues_found = []
    
    if "❌ Node.js NOT installed" in output:
        issues_found.append("Node.js is not installed")
    
    if "❌ npm NOT installed" in output:
        issues_found.append("npm is not installed")
    
    if "❌ PM2 NOT installed" in output:
        issues_found.append("PM2 is not installed")
    
    if "❌ dist directory NOT found" in output:
        issues_found.append("TypeScript not compiled (dist folder missing)")
    
    if "❌ No process listening on port 3000" in output:
        issues_found.append("Application not listening on port 3000")
    
    if "❌ Failed to connect to health endpoint" in output:
        issues_found.append("Health endpoint not responding")
    
    if issues_found:
        print("\n⚠️  ISSUES DETECTED:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
        
        print("\n💡 RECOMMENDED ACTIONS:")
        if "TypeScript not compiled" in str(issues_found):
            print("   1. Run: cd /var/www/aifuncheckapp1 && npm run build")
        if "Application not listening on port 3000" in str(issues_found):
            print("   2. Check PM2 logs: pm2 logs aifuncheckapp1")
            print("   3. Restart application: pm2 restart aifuncheckapp1")
        if "PM2 is not installed" in str(issues_found):
            print("   4. Install PM2: npm install -g pm2")
        
        print(f"\n   📞 For automated fix, run: python3 fix-aifuncheckapp1.py")
    else:
        print("\n✅ No critical issues detected!")
        print(f"🌐 Application should be accessible at: http://{ip_address}/api/health")
    
    print("\n" + "="*80)
    
    return 0 if not issues_found else 1

if __name__ == '__main__':
    sys.exit(main())
