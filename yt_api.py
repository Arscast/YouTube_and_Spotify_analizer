# -*- coding: utf-8 -*-
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from dateutil import parser
import logging
import os

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'client_secret.json'
DEVELOPER_KEY = ''
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


class YouTubeClientAuth:
    def __init__(self):
        # This OAuth 2.0 access scope allows for read-only access to the authenticated
        # user's account, but not other types of account access.
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_console()
        self.youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        self.videosList = []

    def get_my_uploads_list(self):
        # Retrieve the contentDetails part of the channel resource for the
        # authenticated user's channel.
        channels_response = self.youtube.channels().list(
            mine=True,
            part='contentDetails'
        ).execute()

        for channel in channels_response['items']:
            # From the API response, extract the playlist ID that identifies the list
            # of videos uploaded to the authenticated user's channel.
            return channel['contentDetails']['relatedPlaylists']['uploads']

        return None

    def list_my_uploaded_videos(self, uploads_playlist_id, date):
        # Retrieve the list of videos uploaded to the authenticated user's channel.
        playlistitems_list_request = self.youtube.playlistItems().list(
            playlistId=uploads_playlist_id,
            part='snippet',
            maxResults=5
        )
        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            # Print information about each video.
            for playlist_item in playlistitems_list_response['items']:
                title = playlist_item['snippet']['title']
                published_at = playlist_item['snippet']["publishedAt"]
                try:
                    video_date = parser.parse(published_at)
                except ValueError:
                    logging.warning("Can't convert video date")
                    continue
                if video_date > date:
                    video_id = playlist_item['snippet']['resourceId']['videoId']
                    self.videosList.append((title, published_at, video_id))
                    print((title, published_at, video_id))

            playlistitems_list_request = self.youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)

    def execute(self, date):
        try:
            uploads_playlist_id = self.get_my_uploads_list()
            if uploads_playlist_id:
                self.list_my_uploaded_videos(uploads_playlist_id, date)
                logging.debug(self.videosList)
                return self.videosList
            else:
                print('There is no uploaded videos playlist for this user.')
        except HttpError as e:
            print('An HTTP error {:d} occurred:\n{:s}'.format(e.resp.status, e.content))


class YouTubeClientNoAuth:
    def __init__(self):
        global DEVELOPER_KEY
        DEVELOPER_KEY = os.environ['DEVELOPER_KEY']
        if DEVELOPER_KEY == '':
            print('Youtube Developer Key is not set, quitting...')
            exit(3)
        self.youtube = build(API_SERVICE_NAME, API_VERSION,
                             developerKey=DEVELOPER_KEY)

    def youtube_search(self, date, query_string):
        # Call the search.list method to retrieve results matching the specified
        # query term.
        search_response = self.youtube.search().list(
            q=query_string,
            part='id,snippet',
            publishedAfter=date,
            maxResults=25
        ).execute()

        videos = []
        # channels = []
        # playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                print((search_result['snippet']['title'],
                      search_result['snippet']['publishedAt'],
                      search_result['id']['videoId']))
                videos.append((search_result['snippet']['title'],
                              search_result['snippet']['publishedAt'],
                              search_result['id']['videoId']))
            # elif search_result['id']['kind'] == 'youtube#channel':
            #     channels.append('%s (%s)' % (search_result['snippet']['title'],
            #                     search_result['id']['channelId']))
            # elif search_result['id']['kind'] == 'youtube#playlist':
            #     playlists.append('%s (%s)' % (search_result['snippet']['title'],
            #                      search_result['id']['playlistId']))
        return videos

    def execute(self, date, query_string):
        try:
            return self.youtube_search(date, query_string)
        except HttpError as e:
            print('An HTTP error {:d} occurred:\n{:s}'.format(e.resp.status, e.content))
