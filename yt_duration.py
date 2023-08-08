from googleapiclient.discovery import build # for YT Data API interaction
import isodate # for parsing video duration strings
import datetime # fot timedelta objects (need the zero value datetime.timedelta())

API_KEY = "<insert your API key here>"

while True:

    PLAYLIST_NAME = input("Enter the name of the playlist: ")

    if PLAYLIST_NAME.lower() == "stop":
        print("Program terminated.")
        break

    PLAYLIST_ID = input("Enter the ID of the playlist: ")

    if PLAYLIST_NAME == "" or PLAYLIST_ID == "" or len(PLAYLIST_ID) != 34 or PLAYLIST_ID[:2] != "PL":
        print("Invalid input. Please try again.")
        continue

    def cur_page_duration(page_response):
        page_duration = datetime.timedelta()
        for item in page_response['items']:
            duration = item['contentDetails']['duration']
            page_duration += isodate.parse_duration(duration)
        return page_duration

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    # This is the first page of the playlist
    prev_page_request = youtube.playlistItems().list(
        part="contentDetails",
        playlistId=PLAYLIST_ID,
        maxResults=50 # minimize number of requests
    )

    total_duration = datetime.timedelta()

    # The loop below will iterate through all pages of the playlist
    while prev_page_request:
        prev_page_response = prev_page_request.execute()
        videos_on_page_request = youtube.videos().list(
            part="contentDetails",
            id=",".join([item['contentDetails']['videoId'] for item in prev_page_response['items']])
        )
        videos_on_page_response = videos_on_page_request.execute()
        
        total_duration += cur_page_duration(videos_on_page_response)
        prev_page_request = youtube.playlistItems().list_next(prev_page_request, prev_page_response)
        
    print(f"Total Duration of the {PLAYLIST_NAME} playlist corresponding to inputted ID {PLAYLIST_ID} is: {total_duration}\n")