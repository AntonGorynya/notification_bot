import json
import requests
import environs

URL = 'https://dvmn.org/api/user_reviews/'



if __name__ == '__main__':
    env = environs.Env()
    env.read_env()

    headers = {
        'Authorization': env('TOKEN')
    }
    response = requests.get(URL, headers=headers)
    print(json.dumps(response.json(), indent=2))