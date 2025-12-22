# 🔧 Troubleshooting Guide - SND Video Upload Feature

## Common Issues and Solutions

---

## 1. Backend Server Issues

### ❌ Error: "Cannot find module 'express'"
**Cause:** Dependencies not installed

**Solution:**
```bash
cd c:\Users\emroa\Downloads\SND\server
npm install
```

---

### ❌ Error: "Port 3001 is already in use"
**Cause:** Another application is using port 3001

**Solutions:**
1. **Kill the process:**
```bash
# Find process using port 3001
netstat -ano | findstr :3001

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

2. **Change port:**
Edit `.env`:
```env
PORT=3002
```
Then update frontend API URL in [admin.html](file:///c%3A/Users/emroa/Downloads/SND/app/src/main/assets/admin.html) line ~2076:
```javascript
const API_URL = 'http://localhost:3002/api/upload-to-telegram';
```

---

### ❌ Error: "TELEGRAM_BOT_TOKEN is not configured"
**Cause:** Missing or incorrect `.env` file

**Solution:**
1. Check if `.env` exists in `/server` directory
2. Verify content:
```env
TELEGRAM_BOT_TOKEN=8590374410:AAHbu4ZY6-R26wLL5ACE2beQ9VyJuYvxp58
TELEGRAM_CHAT_ID=@soundora_storage
PORT=3001
```
3. Restart server

---

## 2. Telegram Bot Issues

### ❌ Error: "Forbidden: bot can't send messages to the chat"
**Cause:** Bot is not admin in the channel/group

**Solution:**
1. Open your Telegram channel/group
2. Go to Settings → Administrators
3. Add bot as administrator
4. Grant "Post Messages" permission
5. Retry upload

---

### ❌ Error: "Bad Request: chat not found"
**Cause:** Incorrect `TELEGRAM_CHAT_ID`

**Solutions:**
1. **For public channels:** Use `@channel_name`
   ```env
   TELEGRAM_CHAT_ID=@soundora_storage
   ```

2. **For private channels/groups:** Get numeric ID
   - Send a message to your channel
   - Forward it to [@userinfobot](https://t.me/userinfobot)
   - Copy the ID (e.g., `-1001234567890`)
   ```env
   TELEGRAM_CHAT_ID=-1001234567890
   ```

3. **Verify bot is member:**
   - Add bot to channel/group first
   - Then make it admin

---

### ❌ Error: "Telegram API timeout"
**Cause:** Large file upload taking too long

**Solution:**
- This is expected for files >1GB
- Wait for completion (timeout set to 10 minutes)
- For production, increase timeout in `server.js`:
```javascript
timeout: 1800000 // 30 minutes
```

---

## 3. Frontend Upload Issues

### ❌ Error: "Server not running" in browser
**Cause:** Backend server not started

**Solution:**
1. Check server status:
```bash
# In browser, visit:
http://localhost:3001/api/health
```

2. Start server if not running:
```bash
cd c:\Users\emroa\Downloads\SND\server
npm start
```

3. Look for this output:
```
🚀 Server is running on http://localhost:3001
📡 Upload endpoint: http://localhost:3001/api/upload-to-telegram
🤖 Telegram Bot Token: ✅ Configured
```

---

### ❌ Error: "Network error" or "Failed to fetch"
**Cause:** CORS issue or server unreachable

**Solutions:**
1. **Verify server is running:**
```bash
curl http://localhost:3001/api/health
```

2. **Check CORS settings** in `server.js`:
```javascript
app.use(cors({
    origin: ['http://localhost:3000', 'http://127.0.0.1:3000'],
    credentials: true
}));
```

3. **Add your domain** if accessing from different origin:
```javascript
origin: ['http://localhost:3000', 'http://youromain.com'],
```

4. **Disable browser extensions** that might block requests (ad blockers, privacy extensions)

---

### ❌ Progress bar stuck at 0%
**Cause:** Upload not starting properly

**Solution:**
1. Check browser console for errors (F12 → Console)
2. Verify file is selected (check `selectedVideoFile` variable)
3. Ensure server is running
4. Try with smaller test file first (< 100MB)

---

### ❌ Upload succeeds but video URL not filled
**Cause:** JavaScript not finding the quality field

**Solution:**
Check quality selector matches quality field ID:
- Selected quality: `1080p`
- Field ID should be: `source-1080p`

If mismatched, adjust in JavaScript (around line 2131 in [admin.html](file:///c%3A/Users/emroa/Downloads/SND/app/src/main/assets/admin.html)):
```javascript
const qualityFieldId = `source-${selectedQuality.toLowerCase()}`;
```

---

## 4. File Upload Issues

### ❌ Error: "File too large. Maximum size is 2GB"
**Cause:** File exceeds Telegram's limit

**Solutions:**
1. **Compress video:**
```bash
# Using FFmpeg
ffmpeg -i input.mp4 -vcodec h264 -acodec aac -b:v 2M output.mp4
```

2. **Split video into parts:**
```bash
# Split into 30-minute segments
ffmpeg -i input.mp4 -c copy -map 0 -segment_time 00:30:00 -f segment output%03d.mp4
```

3. **Use external storage** for very large files (S3, Azure Blob, etc.)

---

### ❌ Error: "Only video files are allowed"
**Cause:** File type validation failed

**Solution:**
- Ensure file has video MIME type (video/mp4, video/avi, etc.)
- Convert file to MP4 if needed:
```bash
ffmpeg -i input.avi output.mp4
```

---

### ❌ Upload completes but no file_id returned
**Cause:** Telegram response parsing issue

**Solution:**
1. Check server console for error messages
2. Verify bot permissions in channel
3. Test bot with [@userinfobot](https://t.me/userinfobot)
4. Review Telegram API response in server logs

---

## 5. Firestore Integration Issues

### ❌ Video uploads but doesn't save to Firestore
**Cause:** Manual save required

**Current Behavior:**
- Upload returns `file_id` and `videoUrl`
- Admin panel auto-fills the source URL field
- User must click "Save" button to store in Firestore

**Future Enhancement:**
Add Firebase Admin SDK to backend for auto-save:

1. **Install Firebase Admin:**
```bash
npm install firebase-admin
```

2. **Add to server.js:**
```javascript
const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// After Telegram upload success:
await db.collection('videos').add({
  title,
  file_id,
  uploadedBy,
  source: 'telegram',
  createdAt: admin.firestore.FieldValue.serverTimestamp()
});
```

---

## 6. Performance Issues

### ❌ Slow upload speed
**Causes & Solutions:**

1. **Network speed:** Test internet connection
2. **File size:** Consider compression
3. **Telegram server load:** Retry during off-peak hours
4. **Multiple concurrent uploads:** Upload one at a time

---

### ❌ Server crashes during upload
**Cause:** Memory overflow for large files

**Solution:**
Already handled by Multer memory storage, but if issues persist:

1. **Increase Node.js memory:**
```bash
node --max-old-space-size=4096 server.js
```

2. **Use disk storage instead of memory:**
In `server.js`, change:
```javascript
const storage = multer.diskStorage({
    destination: './temp',
    filename: (req, file, cb) => {
        cb(null, Date.now() + '-' + file.originalname);
    }
});
```

---

## 7. Browser-Specific Issues

### ❌ Upload doesn't work in Safari
**Cause:** CORS or FormData compatibility

**Solution:**
- Ensure server CORS includes Safari origin
- Test in Chrome/Edge first to isolate issue
- Update Safari to latest version

---

### ❌ Drag & drop not working
**Cause:** Browser security or JavaScript error

**Solution:**
1. Check browser console for errors
2. Verify `input[type="file"]` has correct attributes
3. Use click-to-select as alternative

---

## 8. Production Deployment Issues

### ❌ Server works locally but not on VPS
**Causes & Solutions:**

1. **Firewall blocking port:**
```bash
# Ubuntu/Debian
sudo ufw allow 3001

# CentOS/RHEL
sudo firewall-cmd --add-port=3001/tcp --permanent
sudo firewall-cmd --reload
```

2. **Wrong Node version:**
```bash
node --version  # Should be v16+
```

3. **Environment variables not loaded:**
```bash
# Check .env is in correct directory
ls -la /path/to/server/.env
```

4. **Process not running:**
```bash
# Use PM2 for process management
pm2 start server.js --name snd-upload
pm2 startup
pm2 save
```

---

### ❌ HTTPS/SSL issues
**Cause:** Browser blocks mixed content (HTTPS → HTTP)

**Solution:**
1. **Setup SSL for backend:**
```javascript
const https = require('https');
const fs = require('fs');

const options = {
    key: fs.readFileSync('server.key'),
    cert: fs.readFileSync('server.cert')
};

https.createServer(options, app).listen(3001);
```

2. **Use reverse proxy (Nginx):**
```nginx
location /api {
    proxy_pass http://localhost:3001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
}
```

---

## 9. Debugging Tips

### Enable Verbose Logging

**Frontend:**
Open browser console (F12) and check:
- Network tab for API calls
- Console tab for JavaScript errors

**Backend:**
Add logging in `server.js`:
```javascript
console.log('File received:', req.file);
console.log('Metadata:', req.body);
console.log('Telegram response:', telegramResponse.data);
```

---

### Test API Directly

Use curl or Postman:
```bash
# Test health endpoint
curl http://localhost:3001/api/health

# Test file upload
curl -X POST http://localhost:3001/api/upload-to-telegram \
  -F "video=@/path/to/test.mp4" \
  -F "title=Test Video" \
  -F "uploadedBy=test_user" \
  -F "userRole=admin" \
  -F "quality=720p"
```

---

## 10. Getting Help

### Useful Resources:
- **Telegram Bot API Docs:** https://core.telegram.org/bots/api
- **Multer Documentation:** https://github.com/expressjs/multer
- **Express.js Guide:** https://expressjs.com/
- **Node.js Docs:** https://nodejs.org/docs/

### Check Logs:
1. **Server logs:** Terminal where server is running
2. **Browser logs:** F12 → Console
3. **Telegram bot logs:** [@BotFather](https://t.me/BotFather) → /mybots → Your Bot → Bot Settings

### Community Support:
- Check GitHub issues (if applicable)
- Telegram developer community
- Stack Overflow with tags: [node.js], [telegram-bot], [multer]

---

## Quick Diagnostic Checklist

- [ ] Node.js installed (v16+)
- [ ] Server dependencies installed (`npm install`)
- [ ] `.env` file exists with correct values
- [ ] Telegram bot token is valid
- [ ] Bot is admin in channel/group
- [ ] Channel ID is correct (with @ for public)
- [ ] Server is running on port 3001
- [ ] Health endpoint responds: `http://localhost:3001/api/health`
- [ ] Browser console shows no CORS errors
- [ ] File size < 2GB
- [ ] File type is video/*
- [ ] Internet connection is stable

---

**Still having issues?** Review server logs and browser console for specific error messages, then search this guide for matching solutions.
