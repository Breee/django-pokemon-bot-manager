import requests
import sys
import time


if __name__ == "__main__":
    try:
        while True:
            for i in range(0, int(sys.argv[1]), 1):
                r = requests.get('http://nginx/bot/status?bot=' + str(i))
                if r.status_code == 200:
                    r = requests.get('http://nginx/bot/output/pull?bot=' + str(i))
            time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
