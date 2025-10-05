import requests
import json
import os
import time
from datetime import datetime
import re
import html
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from PIL import Image, ImageTk
import sys

class DiscordChatArchiverUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Discord DM Archiver Pro")
        self.root.geometry("1000x800")
        self.root.configure(bg='#1e1e2e')
        self.root.minsize(900, 700)
        
        
        self.archiver = None
        self.is_running = False
        
        
        self.setup_styles()
        
        
        self.create_ui()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        
        self.colors = {
            'bg_dark': '#1e1e2e',
            'bg_card': '#2a2a3c',
            'bg_accent': '#3e3e5c',
            'text_primary': '#ffffff',
            'text_secondary': '#a5a5c7',
            'text_accent': '#cba6f7',
            'success': '#a6e3a1',
            'warning': '#f9e2af',
            'error': '#f38ba8',
            'progress': '#89b4fa',
            'purple': '#cba6f7',
            'blue': '#89b4fa',
            'green': '#a6e3a1',
            'yellow': '#f9e2af',
            'red': '#f38ba8',
            'pink': '#f5c2e7',
            'teal': '#94e2d5'
        }
        
       
        self.style.configure('TFrame', background=self.colors['bg_dark'])
        self.style.configure('TLabel', background=self.colors['bg_dark'], 
                           foreground=self.colors['text_primary'], font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', background=self.colors['bg_dark'], 
                           foreground=self.colors['text_accent'], font=('Segoe UI', 20, 'bold'))
        self.style.configure('Subtitle.TLabel', background=self.colors['bg_dark'], 
                           foreground=self.colors['text_secondary'], font=('Segoe UI', 12))
        
        
        self.style.configure('Card.TFrame', background=self.colors['bg_card'], relief='raised', borderwidth=2)
        
        
        self.style.configure('Accent.TButton', 
                           background=self.colors['purple'], 
                           foreground=self.colors['bg_dark'],
                           font=('Segoe UI', 11, 'bold'), 
                           borderwidth=0, 
                           focuscolor='none')
        self.style.map('Accent.TButton', 
                      background=[('active', self.colors['pink']), 
                                ('pressed', self.colors['teal'])])
        
        self.style.configure('Stop.TButton', 
                           background=self.colors['red'], 
                           foreground=self.colors['bg_dark'],
                           font=('Segoe UI', 10, 'bold'))
        self.style.map('Stop.TButton', 
                      background=[('active', '#e78284'), 
                                ('pressed', '#ea999c')])
        
       
        self.style.configure('TEntry', 
                           fieldbackground=self.colors['bg_accent'], 
                           foreground=self.colors['text_primary'],
                           borderwidth=2, 
                           relief='solid',
                           focuscolor=self.colors['purple'])
        
        
        self.style.configure('TProgressbar', 
                           background=self.colors['progress'],
                           troughcolor=self.colors['bg_accent'],
                           borderwidth=0,
                           lightcolor=self.colors['blue'],
                           darkcolor=self.colors['blue'])
        
    def create_ui(self):
        
        main_frame = ttk.Frame(self.root, padding="25")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 25))
        
        
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(anchor='w')
        
        title_label = ttk.Label(title_frame, text="🚀 Discord DM Archiver Pro", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(title_frame, 
                                 text="Discord DM Archiver", 
                                 style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(8, 0))
        
        
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        
        left_panel = ttk.Frame(content_frame, width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 15))
        
        
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        
        
        
        token_card = ttk.Frame(left_panel, style='Card.TFrame', padding="20")
        token_card.pack(fill=tk.X, pady=(0, 15))
        
        card_title = ttk.Label(token_card, text="🔑 Authentication", 
                              foreground=self.colors['blue'], 
                              font=('Segoe UI', 13, 'bold'))
        card_title.pack(anchor='w', pady=(0, 12))
        
        token_help = ttk.Label(token_card, 
                             text="Get your token: F12 → Application → Storage → Local Storage → discord.com → token",
                             foreground=self.colors['text_secondary'], 
                             font=('Segoe UI', 9), 
                             wraplength=360)
        token_help.pack(anchor='w', pady=(0, 15))
        
        
        token_frame = ttk.Frame(token_card)
        token_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.token_var = tk.StringVar()
        self.token_entry = ttk.Entry(token_frame, textvariable=self.token_var, show="•", 
                                   font=('Consolas', 10), width=40)
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.show_token_var = tk.BooleanVar()
        show_token_btn = ttk.Checkbutton(token_frame, text="👁️", 
                                       variable=self.show_token_var,
                                       command=self.toggle_token_visibility)
        show_token_btn.pack(side=tk.RIGHT)
        
        
        output_card = ttk.Frame(left_panel, style='Card.TFrame', padding="20")
        output_card.pack(fill=tk.X, pady=(0, 15))
        
        output_title = ttk.Label(output_card, text="📁 Output Settings", 
                               foreground=self.colors['green'], 
                               font=('Segoe UI', 13, 'bold'))
        output_title.pack(anchor='w', pady=(0, 12))
        
        
        dir_frame = ttk.Frame(output_card)
        dir_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(dir_frame, text="Save to:", font=('Segoe UI', 10, 'bold')).pack(anchor='w')
        
        dir_select_frame = ttk.Frame(dir_frame)
        dir_select_frame.pack(fill=tk.X, pady=(8, 0))
        
        self.output_dir_var = tk.StringVar(value=os.path.join(os.getcwd(), "discord_archives"))
        dir_entry = ttk.Entry(dir_select_frame, textvariable=self.output_dir_var)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(dir_select_frame, text="📂", width=4, command=self.browse_directory)
        browse_btn.pack(side=tk.RIGHT)
        
       
        control_card = ttk.Frame(left_panel, style='Card.TFrame', padding="20")
        control_card.pack(fill=tk.X)
        
        control_title = ttk.Label(control_card, text="⚡ Controls", 
                                foreground=self.colors['yellow'], 
                                font=('Segoe UI', 13, 'bold'))
        control_title.pack(anchor='w', pady=(0, 15))
        
        button_frame = ttk.Frame(control_card)
        button_frame.pack(fill=tk.X)
        
        self.start_btn = ttk.Button(button_frame, text="🎯 Start Archiving", 
                                  command=self.start_archiving, style='Accent.TButton', width=20)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="🛑 Stop", 
                                 command=self.stop_archiving, style='Stop.TButton', state='disabled')
        self.stop_btn.pack(side=tk.LEFT)
        
        
        stats_card = ttk.Frame(left_panel, style='Card.TFrame', padding="20")
        stats_card.pack(fill=tk.X, pady=(15, 0))
        
        stats_title = ttk.Label(stats_card, text="📊 Statistics", 
                              foreground=self.colors['teal'], 
                              font=('Segoe UI', 13, 'bold'))
        stats_title.pack(anchor='w', pady=(0, 12))
        
        self.stats_frame = ttk.Frame(stats_card)
        self.stats_frame.pack(fill=tk.X)
        
       
        self.total_chats_var = tk.StringVar(value="Total Chats: 0")
        self.archived_var = tk.StringVar(value="Archived: 0")
        self.failed_var = tk.StringVar(value="Failed: 0")
        
        ttk.Label(self.stats_frame, textvariable=self.total_chats_var, 
                font=('Segoe UI', 10)).pack(anchor='w')
        ttk.Label(self.stats_frame, textvariable=self.archived_var, 
                font=('Segoe UI', 10)).pack(anchor='w', pady=(5, 0))
        ttk.Label(self.stats_frame, textvariable=self.failed_var, 
                font=('Segoe UI', 10)).pack(anchor='w', pady=(5, 0))
        
        
        
        
        progress_card = ttk.Frame(right_panel, style='Card.TFrame', padding="25")
        progress_card.pack(fill=tk.BOTH, expand=True)
        
        progress_title = ttk.Label(progress_card, text="📈 Archiving Progress", 
                                 foreground=self.colors['purple'], 
                                 font=('Segoe UI', 14, 'bold'))
        progress_title.pack(anchor='w', pady=(0, 20))
        
        
        overall_frame = ttk.Frame(progress_card)
        overall_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(overall_frame, text="Overall Progress", 
                font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        self.overall_progress = ttk.Progressbar(overall_frame, mode='determinate',)
        self.overall_progress.pack(fill=tk.X, pady=(10, 5))
        
        progress_labels = ttk.Frame(overall_frame)
        progress_labels.pack(fill=tk.X)
        
        self.overall_label = ttk.Label(progress_labels, text="0% • Ready to start", 
                                     foreground=self.colors['blue'],
                                     font=('Segoe UI', 10, 'bold'))
        self.overall_label.pack(side=tk.LEFT)
        
        
        current_frame = ttk.Frame(progress_card)
        current_frame.pack(fill=tk.X, pady=(0, 25))
        
        ttk.Label(current_frame, text="Current Chat", 
                font=('Segoe UI', 11, 'bold')).pack(anchor='w')
        
        self.current_label = ttk.Label(current_frame, text="Idle", 
                                     foreground=self.colors['text_secondary'],
                                     font=('Segoe UI', 10))
        self.current_label.pack(anchor='w', pady=(5, 8))
        
        self.chat_progress = ttk.Progressbar(current_frame, mode='determinate',)
        self.chat_progress.pack(fill=tk.X, pady=(0, 5))
        
        
        log_frame = ttk.Frame(progress_card)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_header = ttk.Frame(log_frame)
        log_header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(log_header, text="📝 Activity Log", 
                font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)
        
        clear_btn = ttk.Button(log_header, text="Clear Log", 
                             command=self.clear_log, width=10)
        clear_btn.pack(side=tk.RIGHT)
        
        
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                height=15, 
                                                bg=self.colors['bg_accent'], 
                                                fg=self.colors['text_primary'],
                                                insertbackground=self.colors['text_primary'], 
                                                font=('Consolas', 9),
                                                relief='flat', 
                                                borderwidth=2,
                                                padx=10, 
                                                pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
      
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        self.log_text.tag_config('info', foreground=self.colors['blue'])
        self.log_text.tag_config('accent', foreground=self.colors['purple'])
        
        
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_var = tk.StringVar(value="🎉 Ready")
        status_bar = ttk.Label(status_frame, textvariable=self.status_var, 
                             foreground=self.colors['text_secondary'], 
                             font=('Segoe UI', 9))
        status_bar.pack(side=tk.LEFT)
        
        
        version_label = ttk.Label(status_frame, text="v2.0 • By AmirX021 on github", 
                                foreground=self.colors['text_secondary'], 
                                font=('Segoe UI', 9))
        version_label.pack(side=tk.RIGHT)
        
        
        self.reset_stats()
    
    def reset_stats(self):
        """Reset statistics counters"""
        self.total_chats = 0
        self.archived_count = 0
        self.failed_count = 0
        self.update_stats_display()
    
    def update_stats_display(self):
        """Update statistics display"""
        self.total_chats_var.set(f"📊 Total Chats: {self.total_chats}")
        self.archived_var.set(f"✅ Archived: {self.archived_count}")
        self.failed_var.set(f"❌ Failed: {self.failed_count}")
    
    def toggle_token_visibility(self):
        if self.show_token_var.get():
            self.token_entry.config(show="")
        else:
            self.token_entry.config(show="•")
    
    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
    
    def log(self, message, type="info"):
        """Add message to log with colored timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        
        log_config = {
            "error": {"emoji": "❌", "tag": "error"},
            "warning": {"emoji": "⚠️", "tag": "warning"},
            "success": {"emoji": "✅", "tag": "success"},
            "info": {"emoji": "ℹ️", "tag": "info"},
            "accent": {"emoji": "💫", "tag": "accent"}
        }
        
        config = log_config.get(type, log_config["info"])
        
        log_message = f"[{timestamp}] {config['emoji']} {message}\n"
        
        self.log_text.insert(tk.END, log_message, config['tag'])
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, overall_percent, current_task, chat_percent=0):
        """Update progress bars and labels with colorful feedback"""
        self.overall_progress['value'] = overall_percent
        self.chat_progress['value'] = chat_percent
        
        
        if overall_percent < 30:
            color = self.colors['red']
        elif overall_percent < 70:
            color = self.colors['yellow']
        else:
            color = self.colors['green']
        
        self.overall_label.config(text=f"{overall_percent:.1f}% • {current_task}", 
                                foreground=color)
        self.current_label.config(text=f"{current_task}")
        
       
        status_messages = [
            "🚀 Archiving your conversations...",
            "📦 Packing messages into HTML...",
            "🎨 Creating beautiful archives...",
            "⚡ Processing at light speed...",
            "💫 Making magic happen..."
        ]
        
        if overall_percent < 100:
            status_index = int(overall_percent / 20) % len(status_messages)
            self.status_var.set(status_messages[status_index])
        else:
            self.status_var.set("🎉 Archiving complete! Your conversations are ready!")
        
        self.root.update_idletasks()
    
    def start_archiving(self):
        """Start the archiving process in a separate thread"""
        token = self.token_var.get().strip()
        if not token:
            messagebox.showerror("Error", "🔑 Please enter your Discord token")
            return
        
        output_dir = self.output_dir_var.get()
        if not output_dir:
            messagebox.showerror("Error", "📁 Please select an output directory")
            return
        
        
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.is_running = True
        
        
        self.reset_stats()
        self.clear_log()
        
        self.log("Starting Discord DM archiving process...", "accent")
        self.log("⚠️ Remember: Using self-bots is against Discord's Terms of Service", "warning")
        self.log("💡 Tip: Archive during off-peak hours for better performance", "info")
        
       
        thread = threading.Thread(target=self.run_archiving, args=(token, output_dir))
        thread.daemon = True
        thread.start()
    
    def stop_archiving(self):
        """Stop the archiving process"""
        self.is_running = False
        self.stop_btn.config(state='disabled')
        self.log("Archiving process stopped by user", "warning")
        self.status_var.set("⏹️ Archiving stopped by user")
    
    def run_archiving(self, token, output_dir):
        """Run the actual archiving process"""
        try:
            
            self.archiver = DiscordChatArchiver(token)
            
            
            self.log("Authenticating with Discord...", "info")
            self.update_progress(10, "Authenticating")
            
            user_info = self.archiver.get_user_info()
            if not user_info:
                self.log("Failed to authenticate. Please check your token.", "error")
                self.complete_archiving(False)
                return
            
            username = user_info.get('global_name') or user_info.get('username', 'unknown')
            self.log(f"Successfully authenticated as: {username}", "success")
            self.log(f"User ID: {user_info.get('id', 'Unknown')}", "info")
            
            
            self.log("Discovering DM channels...", "info")
            self.update_progress(20, "Finding conversations")
            
            dm_channels = self.archiver.get_dm_channels()
            if not dm_channels:
                self.log("No DM channels found", "warning")
                self.complete_archiving(False)
                return
            
            
            valid_channels = [ch for ch in dm_channels if ch['type'] in [1, 3]]
            self.total_chats = len(valid_channels)
            self.update_stats_display()
            
            self.log(f"Found {self.total_chats} conversations to archive", "success")
            
            if not self.is_running:
                self.log("Archiving stopped by user", "warning")
                return
            
            
            archive_path = os.path.join(output_dir, f"discord_archive_{username}_{int(time.time())}")
            os.makedirs(archive_path, exist_ok=True)
            self.log(f"Output directory: {archive_path}", "info")
            
            
            self.archived_count = 0
            self.failed_count = 0
            
            for i, channel in enumerate(valid_channels):
                if not self.is_running:
                    break
                
                
                other_user = next((r for r in channel.get('recipients', []) 
                                if r['id'] != user_info['id']), None)
                
                if channel['type'] == 1 and other_user:
                    name = other_user.get('global_name') or other_user['username']
                    chat_type = "👤 DM"
                elif channel['type'] == 3:
                    name = channel.get('name') or ", ".join([r.get('global_name') or r['username'] 
                                                           for r in channel.get('recipients', [])])
                    chat_type = "👥 Group"
                else:
                    continue
                
                self.log(f"Processing {chat_type}: {name}", "accent")
                
               
                overall_percent = 25 + (i / self.total_chats) * 65
                self.update_progress(overall_percent, f"Archiving: {name}")
                
               
                messages = self.archiver.get_all_messages(channel['id'])
                
                if messages and self.is_running:
                    try:
                        html_path, user_details = self.archiver.generate_html(channel, messages, archive_path)
                        if html_path:
                            self.archived_count += 1
                            self.log(f"Archived {len(messages)} messages with {name}", "success")
                        else:
                            self.failed_count += 1
                            self.log(f"Failed to generate HTML for {name}", "error")
                    except Exception as e:
                        self.failed_count += 1
                        self.log(f"Error archiving {name}: {str(e)}", "error")
                else:
                    if messages:
                        self.log(f"No new messages for {name}", "warning")
                    else:
                        self.failed_count += 1
                        self.log(f"No messages retrieved for {name}", "error")
                
                
                self.update_progress(overall_percent, f"Completed: {name}", 100)
                self.update_stats_display()
                time.sleep(0.3)  # API rate limiting
            
            
            if self.is_running:
                self.update_progress(100, "Complete!")
                success_rate = (self.archived_count / self.total_chats) * 100 if self.total_chats > 0 else 0
                self.log(f"🎉 Archiving complete! Success rate: {success_rate:.1f}%", "success")
                self.log(f"📁 Archives saved to: {archive_path}", "info")
                self.status_var.set(f"🎉 Complete! {self.archived_count}/{self.total_chats} chats archived")
            else:
                self.log(f"Archiving stopped. Progress saved.", "warning")
                self.status_var.set(f"⏹️ Stopped - {self.archived_count}/{self.total_chats} chats archived")
            
            self.complete_archiving(True)
            
        except Exception as e:
            self.log(f"Unexpected error: {str(e)}", "error")
            self.complete_archiving(False)
    
    def complete_archiving(self, success):
        """Clean up after archiving completes"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        if success:
            self.log("Archiving session finished", "success")
        else:
            self.log("Archiving session finished with errors", "error")


class DiscordChatArchiver:
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://discord.com/api/v9'
        self.user_info = None
        self.user_cache = {}

    def make_request(self, url, method='GET', params=None):
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=params)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limited
                retry_after = response.json().get('retry_after', 5)
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                return self.make_request(url, method, params)
            else:
                print(f"Error {response.status_code}: {response.text}")
                return None

        except Exception as e:
            print(f"Request failed: {e}")
            return None

    def get_user_info(self): 
        """Get information about the current user"""
        if self.user_info:
            return self.user_info
        url = f'{self.base_url}/users/@me'
        self.user_info = self.make_request(url)
        if self.user_info:
            self.user_cache[self.user_info['id']] = self.user_info
        return self.user_info

    def get_dm_channels(self):  
        """Get all DM channels"""
        url = f'{self.base_url}/users/@me/channels'
        return self.make_request(url)

    def get_messages(self, channel_id, limit=100, before=None): 
        """Get messages from a channel"""
        url = f'{self.base_url}/channels/{channel_id}/messages'
        params = {'limit': limit}
        if before:
            params['before'] = before
        return self.make_request(url, params=params)

    def get_all_messages(self, channel_id, limit=None):
        """Get ALL messages from a channel (no limit)"""
        messages = []
        last_message_id = None

        while True:
            new_messages = self.get_messages(channel_id, limit=100, before=last_message_id)
            if not new_messages:
                break

            messages.extend(new_messages)

            if len(new_messages) < 100:
                break

            last_message_id = new_messages[-1]['id']
            time.sleep(0.5)  

        return messages
    def get_avatar_url(self, user):
        """Construct a user's avatar URL"""
        if not user or 'id' not in user:
            return "https://cdn.discordapp.com/embed/avatars/0.png" 
            
        user_id = user['id']
        avatar_hash = user.get('avatar')

        if avatar_hash:
            return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=128"
        else:
            
            discriminator = user.get('discriminator', '0')
            if discriminator == '0': 
                
                index = (int(user_id) >> 22) % 6
                return f"https://cdn.discordapp.com/embed/avatars/{index}.png"
            else: 
                index = int(discriminator) % 5
                return f"https://cdn.discordapp.com/embed/avatars/{index}.png"
                
    def format_content(self, content):
        """Format message content from Discord markdown to HTML"""
        content = html.escape(content)
        
        content = re.sub(r'(https?://[^\s]+)', r'<a href="\1" target="_blank">\1</a>', content)
        
        content = re.sub(r'&lt;@!?(\d+)&gt;', r'<span class="mention">@user</span>', content)
       
        content = re.sub(r'&lt;#(\d+)&gt;', r'<span class="mention">#channel</span>', content)
        
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)
        
        content = re.sub(r'__(.*?)__', r'<u>\1</u>', content)
        
        content = re.sub(r'~~(.*?)~~', r'<s>\1</s>', content)
       
        content = re.sub(r'`(.*?)`', r'<code>\1</code>', content)
        
        content = content.replace('\n', '<br>')
        return content

    def generate_html(self, channel_info, messages, output_path):
        """Generate a beautiful HTML file for the chat"""
        if not messages:
            return

        other_user = next((r for r in channel_info['recipients'] if r['id'] != self.user_info['id']), None)
        
        
        channel_name = ""
        if other_user:
            channel_name = other_user.get('global_name') or other_user['username']
        else:
            channel_name = channel_info.get('name', 'Unknown')

        
        messages.reverse()

        html_content = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Chat with {html.escape(channel_name)}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700&display=swap" rel="stylesheet">
            <style>
                :root {{
                    --dark-background: #36393f; --medium-background: #2f3136; --light-background: #202225;
                    --text-normal: #dcddde; --text-muted: #72767d; --text-link: #00aff4; --mention-color: #7289da;
                }}
                body {{
                    font-family: 'Noto Sans', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: var(--dark-background); color: var(--text-normal); margin: 0;
                }}
                .container {{ display: flex; flex-direction: column; height: 100vh; }}
                .header {{
                    display: flex; align-items: center; padding: 10px 20px; background-color: var(--medium-background);
                    border-bottom: 1px solid var(--light-background); flex-shrink: 0;
                }}
                .header img {{ width: 32px; height: 32px; border-radius: 50%; margin-right: 15px; }}
                .header h2 {{ margin: 0; font-size: 18px; font-weight: 700; color: white; }}
                .search-bar {{
                    margin-left: auto; background-color: var(--light-background); border: none; border-radius: 4px;
                    color: var(--text-normal); padding: 8px 12px; font-size: 14px;
                }}
                .chat-container {{ flex-grow: 1; overflow-y: auto; padding: 0 20px; }}
                .message {{ display: flex; padding: 10px 0; }}
                .message.grouped {{ padding-top: 2px; padding-bottom: 2px; }}
                .message.grouped .message-header, .message.grouped .avatar-container {{ display: none; }}
                .avatar-container {{ flex-shrink: 0; width: 40px; margin-right: 20px; }}
                .avatar {{ width: 40px; height: 40px; border-radius: 50%; }}
                .message-content {{ display: flex; flex-direction: column; }}
                .message-header {{ display: flex; align-items: baseline; margin-bottom: 5px; }}
                .message-author {{ font-weight: 500; color: white; margin-right: 10px; }}
                .message-time {{ font-size: 12px; color: var(--text-muted); }}
                .message-text {{ line-height: 1.4; word-wrap: break-word; }}
                .message-text a {{ color: var(--text-link); text-decoration: none; }}
                .message-text a:hover {{ text-decoration: underline; }}
                .message-text code {{ background-color: var(--light-background); padding: 2px 4px; border-radius: 3px; font-family: monospace; }}
                .mention {{ background-color: rgba(114, 137, 218, 0.3); color: var(--mention-color); padding: 1px 2px; border-radius: 3px; font-weight: 500; }}
                .attachment img {{ max-width: 400px; max-height: 300px; border-radius: 4px; margin-top: 5px; }}
                .footer {{
                    padding: 10px; text-align: center; font-size: 12px; color: var(--text-muted);
                    background-color: var(--medium-background); border-top: 1px solid var(--light-background); flex-shrink: 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <img src="{self.get_avatar_url(other_user)}" alt="Avatar">
                    <h2>{html.escape(channel_name)}</h2>
                    <input type="text" class="search-bar" placeholder="Search...">
                </div>
                <div class="chat-container" id="chat-container">
        '''
        
        last_author_id = None
        for msg in messages:
            author = msg['author']
            author_id = author['id']
            is_grouped = author_id == last_author_id
            
            avatar_url = self.get_avatar_url(author)
            author_name = html.escape(author.get('global_name') or author['username'])
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
            content = self.format_content(msg.get('content', ''))

            message_class = "message grouped" if is_grouped else "message"
            
            html_content += f'''
            <div class="{message_class}" id="message-{msg['id']}">
                <div class="avatar-container">
                    <img src="{avatar_url}" alt="{author_name}" class="avatar">
                </div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-author">{author_name}</span>
                        <span class="message-time">{timestamp}</span>
                    </div>
                    <div class="message-text">{content}</div>
            '''

            for attachment in msg.get('attachments', []):
                if 'url' in attachment:
                    if 'image' in attachment.get('content_type', ''):
                        html_content += f'<div class="attachment"><a href="{attachment["url"]}" target="_blank"><img src="{attachment["url"]}" alt="attachment"></a></div>'
                    else:
                        html_content += f'<div class="attachment-file"><a href="{attachment["url"]}" target="_blank">{attachment.get("filename", "Download")}</a></div>'
            
            html_content += '</div></div>'
            last_author_id = author_id

        html_content += f'''
                </div>
                <div class="footer">Archived on {datetime.now().strftime('%Y-%m-%d')} | {len(messages)} messages</div>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', () => {{
                    const chatContainer = document.getElementById('chat-container');
                    chatContainer.scrollTop = chatContainer.scrollHeight;

                    const searchBar = document.querySelector('.search-bar');
                    searchBar.addEventListener('input', (e) => {{
                        const searchTerm = e.target.value.toLowerCase();
                        document.querySelectorAll('.message').forEach(msg => {{
                            const text = msg.textContent.toLowerCase();
                            msg.style.display = text.includes(searchTerm) ? 'flex' : 'none';
                        }});
                    }});
                }});
            </script>
        </body>
        </html>
        '''

        
        filename_base = "unknown_chat"
        unique_id = channel_info['id']

        if other_user:
           
            filename_base = other_user.get('global_name') or other_user['username']
            unique_id = other_user['id']
        
        
        safe_name = re.sub(r'[^\w.-]', '', filename_base).strip().replace(' ', '_')
        
        
        filename = f"{safe_name or 'user'}_{unique_id}.html"
        filepath = os.path.join(output_path, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created HTML archive: {filename}")
        return filepath, other_user

    def create_index_page(self, archived_chats, base_path):
        """Create an index page with links to all HTML archives"""
        index_html = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Discord DM Archive</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Noto Sans', 'Segoe UI', sans-serif; background-color: #36393f;
                    color: #dcddde; margin: 0; padding: 40px;
                }}
                .container {{ max-width: 800px; margin: 0 auto; }}
                h1 {{ color: white; text-align: center; margin-bottom: 30px; }}
                .chat-list {{ list-style: none; padding: 0; }}
                .chat-item {{
                    background-color: #2f3136; border-radius: 8px; margin-bottom: 10px;
                    transition: background-color 0.2s;
                }}
                .chat-item:hover {{ background-color: #40444b; }}
                .chat-link {{
                    display: flex; align-items: center; color: white;
                    text-decoration: none; font-weight: 700; padding: 15px 20px;
                }}
                .chat-link img {{
                    width: 40px; height: 40px; border-radius: 50%; margin-right: 15px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Discord DM Archive</h1>
                <ul class="chat-list">
        '''
        
        for chat in archived_chats:
            filename = os.path.basename(chat['path'])
            user = chat['user']
            username = html.escape(user.get('global_name') or user['username']) if user else 'Unknown User'
            avatar_url = self.get_avatar_url(user)
            
            index_html += f'''
            <li class="chat-item">
                <a href="{filename}" class="chat-link">
                    <img src="{avatar_url}" alt="{username}'s avatar">
                    <span>Chat with {username}</span>
                </a>
            </li>
            '''
        
        index_html += '</ul></div></body></html>'
        
        with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("Created index.html navigation page.")

def main():
    root = tk.Tk()
    app = DiscordChatArchiverUI(root)
    root.mainloop()

if __name__ == "__main__":
    
    main()