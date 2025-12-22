const express = require('express');
const cors = require('cors');
const multer = require('multer');
const FormData = require('form-data');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors({
    origin: [
        'http://localhost:3000', 
        'http://127.0.0.1:3000', 
        'http://localhost:5501', 
        'http://127.0.0.1:5501',
        'https://soundora-music.web.app',
        'https://soundora-music.firebaseapp.com'
    ],
    credentials: true
}));
app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));

// Configure Multer to use memory storage (no disk storage)
const storage = multer.memoryStorage();
const upload = multer({
    storage: storage,
    limits: {
        fileSize: 2000 * 1024 * 1024 // 2GB limit (Telegram's max is 2GB for bots)
    },
    fileFilter: (req, file, cb) => {
        // Accept video files only
        if (file.mimetype.startsWith('video/')) {
            cb(null, true);
        } else {
            cb(new Error('Only video files are allowed!'), false);
        }
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'Server is running' });
});

// Upload endpoint
app.post('/api/upload-to-telegram', upload.single('video'), async (req, res) => {
    try {
        console.log('📤 Upload request received');
        
        // Check if file exists
        if (!req.file) {
            return res.status(400).json({ 
                success: false, 
                message: 'No video file provided' 
            });
        }

        // Get metadata from request body
        const { 
            title, 
            uploadedBy, 
            userRole,
            quality = '1080p' // Default quality if not provided
        } = req.body;

        if (!title || !uploadedBy) {
            return res.status(400).json({ 
                success: false, 
                message: 'Title and uploadedBy are required' 
            });
        }

        console.log(`📹 Processing video: ${title}`);
        console.log(`📊 File size: ${(req.file.size / 1024 / 1024).toFixed(2)} MB`);

        // Prepare Telegram Bot API request
        const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
        const TELEGRAM_CHAT_ID = process.env.TELEGRAM_CHAT_ID || '@soundora_storage'; // Your channel/chat ID
        
        if (!TELEGRAM_BOT_TOKEN) {
            throw new Error('TELEGRAM_BOT_TOKEN is not configured');
        }

        // Create form data for Telegram API
        const formData = new FormData();
        formData.append('chat_id', TELEGRAM_CHAT_ID);
        formData.append('video', req.file.buffer, {
            filename: `${title.replace(/[^a-zA-Z0-9]/g, '_')}_${quality}_${Date.now()}.mp4`,
            contentType: req.file.mimetype
        });
        formData.append('caption', `📹 ${title}\n👤 Uploaded by: ${uploadedBy}\n📊 Quality: ${quality}`);
        formData.append('supports_streaming', 'true');

        console.log('🚀 Uploading to Telegram...');

        // Upload to Telegram using streaming
        const telegramResponse = await axios.post(
            `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendVideo`,
            formData,
            {
                headers: {
                    ...formData.getHeaders()
                },
                maxContentLength: Infinity,
                maxBodyLength: Infinity,
                timeout: 600000 // 10 minutes timeout for large files
            }
        );

        // Check if upload was successful
        if (!telegramResponse.data.ok) {
            throw new Error('Telegram upload failed: ' + JSON.stringify(telegramResponse.data));
        }

        // Extract file_id from Telegram response
        const file_id = telegramResponse.data.result.video.file_id;
        const file_unique_id = telegramResponse.data.result.video.file_unique_id;
        const duration = telegramResponse.data.result.video.duration;
        const width = telegramResponse.data.result.video.width;
        const height = telegramResponse.data.result.video.height;

        console.log('✅ Upload successful!');
        console.log(`📎 File ID: ${file_id}`);

        // Return metadata to frontend
        res.json({
            success: true,
            message: 'Video uploaded successfully to Telegram',
            data: {
                file_id,
                file_unique_id,
                title,
                source: 'telegram',
                uploadedBy,
                userRole,
                quality,
                duration,
                width,
                height,
                fileSize: req.file.size,
                uploadedAt: new Date().toISOString(),
                // Generate Telegram video URL (this will work if channel is public)
                videoUrl: `https://t.me/${TELEGRAM_CHAT_ID.replace('@', '')}/${telegramResponse.data.result.message_id}`
            }
        });

    } catch (error) {
        console.error('❌ Upload error:', error.message);
        
        // Handle specific error types
        if (error.code === 'LIMIT_FILE_SIZE') {
            return res.status(413).json({
                success: false,
                message: 'File too large. Maximum size is 2GB.'
            });
        }

        if (error.response?.data) {
            return res.status(500).json({
                success: false,
                message: 'Telegram API error: ' + JSON.stringify(error.response.data)
            });
        }

        res.status(500).json({
            success: false,
            message: error.message || 'Upload failed'
        });
    }
});

// Error handling middleware
app.use((error, req, res, next) => {
    if (error instanceof multer.MulterError) {
        if (error.code === 'LIMIT_FILE_SIZE') {
            return res.status(413).json({
                success: false,
                message: 'File too large. Maximum size is 2GB.'
            });
        }
        return res.status(400).json({
            success: false,
            message: error.message
        });
    }
    
    res.status(500).json({
        success: false,
        message: error.message || 'Internal server error'
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Server is running on http://localhost:${PORT}`);
    console.log(`📡 Upload endpoint: http://localhost:${PORT}/api/upload-to-telegram`);
    console.log(`🤖 Telegram Bot Token: ${process.env.TELEGRAM_BOT_TOKEN ? '✅ Configured' : '❌ Missing'}`);
});

module.exports = app;
