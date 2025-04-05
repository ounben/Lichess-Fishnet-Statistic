import requests
import csv
import time
import datetime
import re
import json

def read_fishnet_stats(filename=r"Y:\Fishnet\.fishnet-stats"): # r wegen \ escape Fehler
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Datei {filename} nicht gefunden.")
        return None
    except json.JSONDecodeError:
        print(f"Fehler beim Parsen von {filename}.")
        return None

def extract_json_data(text, regex):
    match = re.search(regex, text)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return None

def lichess_stats_to_csv(filename="lichess_stats.csv"):
    with open(filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        if csv_file.tell() == 0:
            writer.writerow(["Timestamp", "Spieler", "Spiele", "Fishnet_User_Acquired", "Fishnet_User_Queued", "Fishnet_User_Oldest", "Fishnet_System_Acquired", "Fishnet_System_Queued", "Fishnet_System_Oldest", "Total_Batches", "Total_Positions", "Total_Nodes"])

        wait_time = 300  # Anfangswartezeit in Sekunden

        while True:
            try:
                # Lichess-Hauptseite
                response = requests.get("https://lichess.org/")
                response.raise_for_status()
                text = response.text

                # JavaScript-Objekt extrahieren
                data = extract_json_data(text, r'{"data":{.*?},"showRatings":true,"hasUnreadLichessMessage":false}')
                if data:
                    players = data["data"]["counters"]["members"]
                    games = data["data"]["counters"]["rounds"]
                else:
                    print("JavaScript-Daten nicht gefunden.")
                    continue

                # Fishnet-Statusseite
                fishnet_response = requests.get("https://lichess.org/fishnet/status")
                fishnet_response.raise_for_status()
                fishnet_text = fishnet_response.text

                # Fishnet-Werte extrahieren
                fishnet_data = extract_json_data(fishnet_text, r'{"analysis":{"user":{"acquired":\d+,"queued":\d+,"oldest":\d+},"system":{"acquired":\d+,"queued":\d+,"oldest":\d+}}}')
                if fishnet_data:
                    user_acquired = fishnet_data["analysis"]["user"]["acquired"]
                    user_queued = fishnet_data["analysis"]["user"]["queued"]
                    user_oldest = fishnet_data["analysis"]["user"]["oldest"]
                    system_acquired = fishnet_data["analysis"]["system"]["acquired"]
                    system_queued = fishnet_data["analysis"]["system"]["queued"]
                    system_oldest = fishnet_data["analysis"]["system"]["oldest"]
                else:
                    print("Fishnet-Daten nicht gefunden.")
                    continue

                fishnet_local_data = read_fishnet_stats()

                timestamp = datetime.datetime.now().isoformat()
                if fishnet_local_data:
                    writer.writerow([timestamp, players, games, user_acquired, user_queued, user_oldest, system_acquired, system_queued, system_oldest, fishnet_local_data.get("total_batches"), fishnet_local_data.get("total_positions"), fishnet_local_data.get("total_nodes")])
                    print(f"{timestamp}: Spieler={players}, Spiele={games}, Fishnet User Acquired={user_acquired}, Fishnet User Queued={user_queued}, Fishnet User Oldest={user_oldest}, Fishnet System Acquired={system_acquired}, Fishnet System Queued={system_queued}, Fishnet System Oldest={system_oldest}, Total Batches={fishnet_local_data.get('total_batches')}, Total Positions={fishnet_local_data.get('total_positions')}, Total Nodes={fishnet_local_data.get('total_nodes')}")
                else:
                    writer.writerow([timestamp, players, games, user_acquired, user_queued, user_oldest, system_acquired, system_queued, system_oldest, None, None, None])
                    print(f"{timestamp}: Spieler={players}, Spiele={games}, Fishnet User Acquired={user_acquired}, Fishnet User Queued={user_queued}, Fishnet User Oldest={user_oldest}, Fishnet System Acquired={system_acquired}, Fishnet System Queued={system_queued}, Fishnet System Oldest={system_oldest}, Total Batches=None, Total Positions=None, Total Nodes=None")

                csv_file.flush()

                wait_time = 60  # Wartezeit zurücksetzen, wenn erfolgreich

            except requests.exceptions.RequestException as e:
                if e.response and e.response.status_code == 429:
                    print(f"Zu viele Anfragen. Warte {wait_time} Sekunden.")
                    time.sleep(wait_time)
                    wait_time = min(wait_time * 2, 600)  # Exponentielle Backoff (max. 10 Minuten)
                    continue
                else:
                    print(f"Fehler beim Abrufen der Daten: {e}")
            except (ValueError, AttributeError, IndexError, json.JSONDecodeError) as e:
                print(f"Fehler beim Parsen der Daten: {e}")
            except Exception as e:
                print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

            time.sleep(wait_time)

if __name__ == "__main__":
    lichess_stats_to_csv()