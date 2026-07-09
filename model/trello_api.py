import requests

API_KEY = "71e5b5adb25c6f8350f3f28c4cdf1882"

def buscar_cards(token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards?key={API_KEY}&token={token}"
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else []
    except:
        return []

def buscar_listas(token, board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/lists?key={API_KEY}&token={token}"
    try:
        response = requests.get(url)
        return {lista["name"]: lista["id"] for lista in response.json()} if response.status_code == 200 else {}
    except:
        return {}

def concluir_card(token, card_id):
    url = f"https://api.trello.com/1/cards/{card_id}?closed=true&key={API_KEY}&token={token}"
    return requests.put(url).status_code == 200

def criar_card(token, list_id, nome, cor_label):
    url = f"https://api.trello.com/1/cards?idList={list_id}&name={nome}&labels={cor_label}&key={API_KEY}&token={token}"
    return requests.post(url).status_code == 200