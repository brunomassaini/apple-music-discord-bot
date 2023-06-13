from distutils.core import setup
import py2app
import os

client_id = os.getenv('DISCORD_CLIENT_ID')

# Icon file name
#ICON_FILE = 'icon.icns'

# Update the setup configuration
setup(
    app=['bot/main.py'],
    options={
        'py2app': {
            'argv_emulation': True,
            'iconfile':'icon.icns',
            'plist': {
                'CFBundleShortVersionString': '1.0',
                'CFBundleName': 'AppleMusicDiscordBot',
                #'CFBundleIconFile': ICON_FILE,
                'LSEnvironment': {
                    'DISCORD_CLIENT_ID': client_id,
                },
            },
        },
    },
    setup_requires=['py2app'],
)