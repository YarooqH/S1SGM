# Schedule I Save Game Sync Manager

A simple tool to share and manage Schedule I save games with friends. Perfect for when you've played with a friend and want to continue the same game on your own, or when you want to try out different strategies from the same starting point.

## 🎮 Features

- Sync your save games to GitHub
- Download save games from friends
- Create local backups
- Easy-to-use interface
- Automatic save game detection
- Multiple save slot management

## 🚀 Getting Started

### Prerequisites
- Windows PC
- Schedule I game installed
- GitHub account (free)

### Installation
1. Download the latest release from the [Releases](../../releases) page
2. Run `ScheduleISaveSync.exe`
3. First-time setup:
   - Go to the Settings tab
   - Create a GitHub token (instructions provided in the app)
   - Enter your GitHub token
   - Save settings

### How to Use

#### Sharing Your Save Game
1. Play Schedule I with your friend
2. When you want to share the save:
   - Open ScheduleISaveSync
   - Go to "My Saves" tab
   - Click "Sync to GitHub"
3. Share your GitHub repository URL with your friend

#### Using a Friend's Save Game
1. Get your friend's GitHub repository URL
2. In ScheduleISaveSync:
   - Go to "Friends' Saves" tab
   - Add your friend's repository
   - Click "Download Selected Save"
3. Choose whether to:
   - Create a new save slot
   - Replace an existing save

## 💡 Common Use Cases

### Continue a Friend's Game
Played with your friend and want to enjoy the same game again and progress on your own? Just download their save and continue from where you left off!

### Share Strategies
Found an interesting strategy or game state? Share it with your friends so they can try different approaches from the same point.

### Backup Management
Keep your saves safe and organized with local backups and version control through GitHub.

## 🔧 Troubleshooting

### Save Location Not Found
The default save location is: 

C:\Users\[YourUsername]\AppData\LocalLow\TVGS\Schedule I\Saves

If your saves are in a different location, you can set it in the Settings tab.

### GitHub Token Issues
Make sure your token has the following permissions:
- `repo` (Full control of private repositories)
- `workflow`

## 📝 Notes

- Save files are stored in private GitHub repositories by default
- Each user can have multiple save slots
- The app automatically handles different Steam user IDs

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Thanks to the Schedule I community
- Built with Python and tkinter
- Uses PyGithub for GitHub integration