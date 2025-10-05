# 🚀 Discord DM Archiver Pro

A powerful, feature-rich Python application that archives your Discord direct messages into beautiful, searchable HTML files with a modern graphical interface.

![Discord Archiver](https://img.shields.io/badge/Discord-Archiver-purple?style=for-the-badge&logo=discord)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

### 🎨 Beautiful Interface
- **Modern Dark Theme** - Discord-inspired color scheme
- **Colorful Progress Indicators** - Visual feedback with vibrant colors
- **Real-time Statistics** - Live counters for chats archived/failed
- **Emoji-rich Interface** - Visual indicators throughout the app

### 📊 Advanced Archiving
- **Complete Message Capture** - No limits on messages per chat
- **Beautiful HTML Output** - Professionally formatted chat archives
- **Media Preservation** - Images and attachments are saved
- **Search Functionality** - Built-in search in HTML files
- **Group Chat Support** - Handles both DMs and group conversations

### ⚡ Smart Features
- **Real-time Progress Tracking** - Dual progress bars with color coding
- **Rate Limit Handling** - Automatic API rate limit management
- **Error Resilience** - Continues archiving even if some chats fail
- **Batch Processing** - Archives all DMs in one go
- **Organized Output** - Clean folder structure with index page

## 🖼️ Screenshots

<img width="1002" height="825" alt="{6046B641-DFBE-4E6D-A31E-7BF83EC7A189}" src="https://github.com/user-attachments/assets/a3a32ee8-5111-4ec2-81c0-45a537c792a1" />


## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/AmirX021/DiscordChat-Archiver.git
cd DiscordChat-Archiver
```

### Step 2: Install Dependencies
```bash
pip install requests pillow tkinter
```

### Step 3: Get Your Discord Token
1. Open Discord in your browser
2. Press `F12` to open Developer Tools
3. Go to **Application** tab → **Storage** → **Local Storage** → `discord.com`
4. Find the `token` key and copy its value

### Step 4: Run the Application
```bash
python DiscordChat-Archiver.py
```

## 🎯 Usage

1. **Launch the Application** - Run the script to open the graphical interface
2. **Enter Discord Token** - Paste your token in the authentication field
3. **Configure Settings** - Choose output directory (optional)
4. **Start Archiving** - Click "Start Archiving" to begin the process
5. **Monitor Progress** - Watch real-time progress and statistics
6. **Access Archives** - Find your archived chats in the output folder

## 📁 Output Structure

```
discord_archives/
├── discord_archive_username_timestamp/
│   ├── index.html              # Navigation page
│   ├── user_info.json          # Your Discord profile info
│   ├── chat_user12345.html     # Individual chat archives
│   ├── group_chat67890.html
│   └── ...
```

## 🎨 HTML Archive Features

- **Responsive Design** - Works on desktop and mobile
- **Message Grouping** - Groups consecutive messages from same user
- **Media Display** - Shows images and file attachments
- **Search Function** - Built-in message search
- **Timestamps** - Precise message timing
- **User Avatars** - Profile pictures preserved
- **Markdown Support** - Formatting preserved (bold, italic, code, etc.)

## ⚠️ Important Notes

### Legal Disclaimer
> **Warning**: Using self-bots is against Discord's Terms of Service. This tool is intended for educational purposes and personal archiving. Use at your own risk and respect Discord's API rate limits.



## 🐛 Troubleshooting

### Common Issues

1. **"Invalid Token" Error**
   - Ensure you copied the entire token
   - Token should start with your user ID

2. **Rate Limiting**
   - The app automatically handles rate limits
   - If issues persist, wait and try again later

3. **Missing Messages**
   - Some very old messages might not be accessible via API
   - The app retrieves all available messages

4. **Permission Errors**
   - Ensure you have write permissions in the output directory
   - Try running as administrator if needed

## 🔧 Technical Details

### Built With
- **Python** - Core programming language
- **Tkinter** - Graphical user interface
- **Requests** - HTTP API calls
- **PIL** - Image processing (if needed)
- **HTML/CSS** - Archive formatting

### API Endpoints Used
- `/users/@me` - User authentication
- `/users/@me/channels` - Get DM channels
- `/channels/{id}/messages` - Retrieve messages

## 🤝 Contributing

We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Discord API documentation
- Python community for excellent libraries
- Contributors and testers

--

**⭐ If you find this project useful, please give it a star on GitHub!**

--
