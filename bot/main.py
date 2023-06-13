import subprocess
import pypresence
import time
import os

client_id = os.getenv('DISCORD_CLIENT_ID')
apple_music_logo = "https://apple-resources.s3.amazonaws.com/medusa/production/images/5f600674c4f022000191d6c4/en-us-large@1x.png"

RPC = pypresence.Presence(client_id,pipe=0)  # Initialize the client class
rpc_connected = False

def get_current_track():
    command = """
        osascript -e 'tell application "Music"
            if player state is playing then
                set trackName to name of current track
                set artistName to artist of current track
                set albumName to album of current track
                set trackDuration to duration of current track
                set currentPosition to player position
                return trackName & ";" & artistName & ";" & albumName & ";" & trackDuration & ";" & currentPosition
            else
                return ""
            end if
        end tell'
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()
    if output:
        track_info = output.split(";")
        return {
            "track": track_info[0],
            "artist": track_info[1],
            "album": track_info[2],
            "duration": track_info[3],
            "position": track_info[4]
        }
    else:
        return None
    
import requests

def retrieve_album_cover(song_name, artist_name):
    # Prepare the search query
    search_query = f"{song_name} {artist_name}"
    params = {
        'term': search_query,
        'entity': 'song'
    }

    # Send the request to the iTunes Search API
    response = requests.get('https://itunes.apple.com/search', params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Retrieve the first result
        if data['resultCount'] > 0:
            result = data['results'][0]
            album_cover_url = result['artworkUrl100']
            return album_cover_url
        else:
            print("No results found.")
    else:
        print("Request failed.")

    return None

while True:  # The presence will stay on as long as the program is running
    current_track = get_current_track()
    print(rpc_connected)
    print(current_track)

    if current_track != None:
        if rpc_connected == False:
            RPC.connect() # Start the handshake loop

        rpc_connected = True

        current_time = int(time.time())
        album_cover_url = retrieve_album_cover(current_track["track"], current_track["artist"])

        duration_integer = int(current_track["duration"].split(",")[0])
        position_integer = int(current_track["position"].split(",")[0])

        music_started = current_time - position_integer
        music_ends = music_started + duration_integer

        print(RPC.update(
            large_image=(album_cover_url),
            small_image=(apple_music_logo),
            details=current_track["track"],
            state=current_track["artist"],
            start=music_started,
            end=music_ends))  # Set the presence
    else:
        print("No music playing.")
        if rpc_connected == True:
            RPC.close()
            rpc_connected = False
    
    time.sleep(15) # Can only update rich presence every 15 seconds