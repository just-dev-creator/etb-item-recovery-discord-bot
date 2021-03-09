# EtB Item recovery discord bot
### Summary

The EtB Item recovery discord bot allows players of the Minecraft-Server Explore the Build to easily get their items back.
It was developed espacially for this usecase and can't be used for other purposes without modifying the script.

It was developed in Python using pymongo, discord-py-slash-commands and discordpy.

### Download and Install
```bash
# Download
git clone "https://github.com/just-dev-creator/etb-item-recovery-discord-bot" && cd etb-item-recovery-discord-bot

# Install libs and dependencies
pip install -r requirements.txt
```
Then, you need to set the following environment variables:
```dotenv
DISCORD_BOT_TOKEN=YOUR-BOT-TOKEN
MONGODB_CONNECTION_STRING=YOUR-CONNECTION-STRING
``` 

### Run
```bash
python main.py
```
### Upcoming changes
- [X] Make changes for easy use for everyone
- [ ] Create ticket-like conversation