from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests import Session
from subprocess import Popen
import json
import sys
import os


class Epic(Session):
    def __init__(self):
        super().__init__()
        self.headers['User-Agent'] = f'UELauncher/14.3.0-22750546+++Portal+Release-Live Windows/10.0.19041.1.256.64bit'
        self.mount('https://', HTTPAdapter(pool_maxsize=16))

        self.user_data = None

    def login(self, file):
        if file:
            with open(user_file, "r") as f:
                refresh_token = json.load(f)["refresh_token"]
                payload = {'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'token_type': 'eg1'}
        else:
            authcode = input("Enter Auth Code: ")
            payload = {'grant_type': 'authorization_code', 'code': authcode, 'token_type': 'eg1'}

        r = self.post(
            url=f'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/token',
            data=payload,
            auth=HTTPBasicAuth("34a02cf8f4414e29b15921876da36f9a", "daafbccc737745039dffe53d94fc76cf"),
            timeout=10.0
        )

        if r.status_code != 200:
            raise ConnectionError("Token expired!")

        self.user_data = r.json()
        self.headers['Authorization'] = f'bearer {self.user_data["access_token"]}'

        with open(self.user_data["displayName"] + ".json", "w") as f:
            json.dump(self.user_data, f, indent=4)

    def _get_game_token(self):
        r = self.get(f'https://account-public-service-prod03.ol.epicgames.com/account/api/oauth/exchange', timeout=10.0)
        r.raise_for_status()
        return r.json()["code"]

    def launch_game(self, path):
        path = os.path.abspath(path)
        base_path = "\\".join(path.split("\\")[:-1])
        exe = path.split("\\")[-1]

        full_params = [
            base_path + os.sep + exe,
            '-AUTH_LOGIN=unused',
            '-AUTH_PASSWORD=' + self._get_game_token(),
            '-AUTH_TYPE=exchangecode',
            '-epicapp=Sugar',
            '-epicenv=Prod',
            '-EpicPortal',
            '-epicusername=' + self.user_data["displayName"],
            '-epicuserid=' + self.user_data["account_id"],
            '-epiclocale=es',
        ]

        Popen(full_params, cwd=base_path, env=os.environ.copy())


if __name__ == '__main__':
    args = sys.argv[1:]
    user_file = args[args.index("--user_file" if "--user_file" in args else "-u") + 1] if any(f in args for f in ["--user", "-u"]) else None
    game_path = args[args.index("--launch" if "--launch" in args else "-l") + 1] if any(f in args for f in ["--launch", "-l"]) else None

    epic = Epic()
    epic.login(user_file if user_file else None)
    if game_path:
        epic.launch_game(game_path)
