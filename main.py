import requests
from bs4 import BeautifulSoup


def login_to_instacart(email, password):
    session = requests.Session()
    login_url = "https://www.instacart.com/accounts/login"
    response = session.get(login_url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "authenticity_token"}).get("value")

    payload = {
        "user[email]": email,
        "user[password]": password,
        "authenticity_token": csrf_token,
    }

    response = session.post(login_url, data=payload)
    if "Sign Out" in response.text:
        print("Logged in successfully")
        return session
    else:
        print("Login failed")
        return None


def add_card(session, card_number):
    add_card_url = "https://www.instacart.com/accounts/payment_methods"
    response = session.get(add_card_url)
    soup = BeautifulSoup(response.text, "html.parser")
    csrf_token = soup.find("input", {"name": "authenticity_token"}).get("value")

    payload = {
        "payment_method[card_number]": card_number,
        "authenticity_token": csrf_token,
    }

    response = session.post(add_card_url, data=payload)
    if "Card added successfully" in response.text:
        return True, None
    else:
        error_message = soup.find("div", {"class": "error-message"}).text
        return False, error_message


def process_cards(email, password):
    session = login_to_instacart(email, password)
    if not session:
        return

    with open("cards.txt", "r") as cards_file, open(
        "added.txt", "a"
    ) as added_file, open("fail.txt", "a") as fail_file:
        for card in cards_file:
            card = card.strip()
            success, error_message = add_card(session, card)
            if success:
                added_file.write(f"{card}\n")
            else:
                fail_file.write(f"{card} - {error_message}\n")


if __name__ == "__main__":
    email = input("Enter your Instacart email: ")
    password = input("Enter your Instacart password: ")
    process_cards(email, password)
