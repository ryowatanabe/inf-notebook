from sys import argv
import json

from main import generate_data,api_request

if __name__ == '__main__':
    if argv[1] == 'test':
        data = generate_data([12])
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    if argv[1] == 'songs12':
        data = api_request('songs', params={'level': '12'})
        with open('songs12.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    if argv[1] == 'data12':
        data = api_request('data', params={'level': '12'})
        with open('data12.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
