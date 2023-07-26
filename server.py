import socket 
import pickle 
import grequests
from bs4 import BeautifulSoup
import pandas as pd 

ids = ['skill-moves', 'attacking-work-rate', 'defensive-work-rate', 'foot']

classes_names = ['Name', 'Pac', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'SM', 'AWR', 'DWR', 'FOOT']


def get_all_urls(): 
        all_urls = []
        for curr_page in range(1, 21):
            all_urls.append(f'https://www.fifplay.com/fifa-22/players/?page={curr_page}')
        return all_urls


def extract_raw_data(all_urls): 
    all_requests = []
    for page_link in all_urls: 
        all_requests.append(grequests.get(page_link))
    all_requests = grequests.map(all_requests)
    return all_requests

def extract_info(footballer): 
    
        info = [] 
        info.append(footballer.find('td', class_ = 'name').text[1:].partition('\n')[0])

        football_features = footballer.find_all('div', class_ = 'stats-main')
    
        for i in range(1, 7): 
            info.append(football_features[i-1].text)
    
        for curr_id in ids: 
            info.append(footballer.find('td', id = curr_id).text.replace('\n', ''))
    
        return info

def parse_data(all_requests): 
    
    all_info = [] 
    for curr_req in all_requests:
        
        soup = BeautifulSoup(curr_req.text, 'lxml')

        footballers = soup.find_all('tr', class_ = 'clickable')

        page_info = [] 

        for footballer in footballers: 
            page_info.append(extract_info(footballer))
            
        all_info.append(page_info)
        
    return sum(all_info, [])

def create_dataframe(all_info):
    df = pd.DataFrame(all_info, columns = classes_names)
    return df 
    
def run(n):
    all_urls = get_all_urls()
    all_requests = extract_raw_data(all_urls)
    all_info = parse_data(all_requests)
    df = create_dataframe(all_info)
    return df.head(n)

HEADERSIZE = 10
PORT = 1000 
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(5)


while True: 
    clientsocket, address = server.accept() 
    print(f"Connection from {address} has been established")

    msg_r = clientsocket.recv(16)
    msg_r = int(msg_r.decode())
    obj = run(msg_r) 

    msg = pickle.dumps(obj)
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', FORMAT) + msg

    clientsocket.send(msg) 

