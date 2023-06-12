from distutils.core import setup
import py2app
import os

client_id = os.getenv('DISCORD_CLIENT_ID')

# Update the setup configuration
setup(
    app=['bot/main.py'],
    options={
        'py2app': {
            'argv_emulation': True,
            'plist': {
                'CFBundleShortVersionString': '1.0',
                'CFBundleName': 'AppleMusicDiscordBot',
                'LSEnvironment': {
                    'DISCORD_CLIENT_ID': client_id,
                },
            },
        },
    },
    setup_requires=['py2app'],
)