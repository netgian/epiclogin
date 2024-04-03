# Epic Games Launcher Automation

This Python script provides automation capabilities for launching Epic Games via command-line interface. It facilitates logging in to the Epic Games account and launching a specified game.

## Prerequisites
- Python 3.x
- `requests` library (`pip install requests`)

## Usage

```bash
python epiclogin.py --user_file or -u <user_file.json> --launch or -l <game_path>
```

You got to provide your authcode from here: [epicgames.com](https://www.epicgames.com/id/login?redirectUrl=https%3A//www.epicgames.com/id/api/redirect%3FclientId%3D34a02cf8f4414e29b15921876da36f9a%26responseType%3Dcode)


## Tested on:
- Windows 10


This project is distributed under [GNU General Public License v3.0](https://github.com/netgian/epiclogin/blob/main/LICENSE) license.
