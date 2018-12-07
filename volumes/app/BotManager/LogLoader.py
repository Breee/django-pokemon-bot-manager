import requests
import sys
import time


if __name__ == "__main__":
    try:
        while True:
            for i in range(0, int(sys.argv[1]), 1):
                r = None
                try:
                    r = requests.get('http://nginx/bot/status?bot=' + str(i))
                except requests.exceptions.Timeout:
                    pass
                except requests.exceptions.TooManyRedirects:
                    pass
                except requests.exceptions.RequestException as e:
                    # catastrophic error. bail.
                    print(e)

                if r is not None:
                    if r.status_code == 200:
                        r = requests.get('http://web:8000/bot/output/pull?bot=' + str(i))
            time.sleep(1)
    except KeyboardInterrupt:
        print('interrupted!')
