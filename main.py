# -*- coding: utf-8 -*-

from yt_api import YouTubeClientAuth, YouTubeClientNoAuth
from spotify_api import SpotifyClient
from dateutil import parser
from openpyxl import Workbook
import pytz
import logging


def write_dict_to_xlsx_file(dict_to_save, headers, path='output.xlsx'):
    """
    Writes dictionary to XLSX (MS Excel spreadsheet) file

    Args:
    dict_to_save - what to save
    headers - headers row
    path - path to save file to

    Example call:
    write_dict_to_xlsx_file(mydict, ("column1",  "column2"), 'output.xlsx')
    """
    logging.debug('write_dict_to_xlsx_file with parms: {}, {}, {}'.format(dict_to_save, headers, path))
    wb = Workbook()
    sheet = wb.active
    sheet.append(headers)
    for row in dict_to_save:
        sheet.append(row)
    wb.save(path)


def save_to_a_file():
    """
    Asks user if it is needed to save results to a file.

    Returns
    file name (path)
    """
    # TBD - check if path is writable with os.access(path, os.W_OK)
    result = input("czy zapisać do pliku xls (jeśli tak podaj nazwę pliku):")
    logging.debug("save_to_a_file: {}".format(result))
    return result


def get_date():
    """
    Get date from user for use in filters
    """
    date = pytz.utc.localize(parser.parse("01/01/1900"))
    while date == pytz.utc.localize(parser.parse("01/01/1900")):
        try:
            date = pytz.utc.localize(parser.parse(input("Podaj datę od której mają być pobrane dane (DD/MM/YYYY): ")))
        except ValueError:
            tryagain = input("Wrong input, want try again (Y/n)?")
            if tryagain in ["Y", "y", ""]:
                date = pytz.utc.localize(parser.parse("01/01/1900"))
            else:
                quit(2)
    print("You entered: {}".format(date))
    return date


def main():
    source = "0"
    while source not in ["1", "2", "3", "Q", "q"]:
        source = input("Wybierz zrodło : \n1 - YouTube (authorized request), 2 - Youtube (no auth), 3 - Spotify: ")
        if source == "1":
            print("You selected: YouTube (auth)")
            yt_client = YouTubeClientAuth()
            videos_list = yt_client.execute(get_date())
            write_to_file = save_to_a_file()
            if write_to_file != "":
                write_dict_to_xlsx_file(videos_list, ("title", "publishedAt", "video_id"), write_to_file)
        elif source == "2":
            print("You selected: YouTube (no auth)")
            yt_client = YouTubeClientNoAuth()
            filter_date = get_date()
            query_string = input('Enter query string (default "Google Developers"): ')
            if query_string == "":
                query_string = "Google Developers"
            videos_list = yt_client.execute(filter_date.isoformat(), query_string)
            write_to_file = save_to_a_file()
            if write_to_file != "":
                write_dict_to_xlsx_file(videos_list, ("title", "publishedAt", "video_id"), write_to_file)
        elif source == "3":
            print("You selected: Spotify")
            sp_client = SpotifyClient()
            artist = input("Specify artist name (default - Abba): ")
            if artist == "":
                artist = "Abba"
            date_range = input('Specify years range (default "1976-1979"): ')
            if date_range == "":
                date_range = "1976-1979"
            tracks = sp_client.get_playlists(artist=artist, date_range=date_range)
            write_to_file = save_to_a_file()
            if write_to_file != "":
                write_dict_to_xlsx_file(tracks, ('id', 'artists', 'track name', 'release_date', 'href'), write_to_file)
        else:
            print("Nie prawidłowe dane! Please enter 1/2/3 or 'Q' for quit")
    exit(0)


if __name__ == "__main__":
    main()
