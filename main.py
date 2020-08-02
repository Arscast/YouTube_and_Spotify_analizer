# -*- coding: utf-8 -*-

from yt_api import YT_client, YT_client1
from spotify_api import Spotify_client
from dateutil import parser
from openpyxl import Workbook
import pytz
import logging


def write_dict_to_xlsx_file(dict_to_save, headers, path='output.xlsx'):
    """
    Writes dictionary to XLSX (MS Excel spreadsheet) file
    Paramters:
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
    Returns file name (path)
    """
    # TBD - check if path is writable with os.access(path, os.W_OK)
    result = input("czy zapisać do pliku xls (jeśli tak podaj nazwę pliku):")
    logging.debug("save_to_a_file: {}".format(result))
    return result


def main():
    source = "0"
    while source not in ["1", "2", "3", "Q", "q"]:
        source = input("Wybierz zrodło : \n1 - YouTube (authorized request), 2 - Youtube (no auth), 3 - Spotify: ")
        if source == "1":
            print("Wybrane: YouTube (auth)")
            date = pytz.utc.localize(parser.parse("01/01/1900"))
            while date == pytz.utc.localize(parser.parse("01/01/1900")):
                try:
                    date = pytz.utc.localize(parser.parse(input("Podaj datę od której mają być pobrane dane (DD/MM/YYYY): ")))
                except ValueError:
                    tryagain = input("Nieprawidłowy dane, chcesz sprobować znowu (Y/n)?")
                    if tryagain in ["Y", "y", ""]:
                        date = pytz.utc.localize(parser.parse("01/01/1900"))
                    else:
                        quit(2)
            print("Wprowadziłeś: {}".format(date))
            ytClient = YT_client()
            videosList = ytClient.execute(date)
            writeToFile = save_to_a_file()
            if writeToFile != "":
                write_dict_to_xlsx_file(videosList, ("title", "publishedAt", "video_id"), writeToFile)
        elif source == "2":
            print("Wybrane: YouTube (no auth)")
            date = pytz.utc.localize(parser.parse("01/01/1900"))
            while date == pytz.utc.localize(parser.parse("01/01/1900")):
                try:
                    date = pytz.utc.localize(parser.parse(input("Podaj datę od której mają być pobrane dane (DD/MM/YYYY): ")))
                except ValueError:
                    tryagain = input("Nieprawidłowy dane, chcesz sprobować znowu (Y/n)?")
                    if tryagain in ["Y", "y", ""]:
                        date = pytz.utc.localize(parser.parse("01/01/1900"))
                    else:
                        quit(2)
            print("Wprowadziłeś: {}".format(date.isoformat()))
            ytClient = YT_client1()
            videosList = ytClient.execute(date.isoformat())
            writeToFile = save_to_a_file()
            if writeToFile != "":
                write_dict_to_xlsx_file(videosList, ("title", "publishedAt", "video_id"), writeToFile)
        elif source == "3":
            print("Wybrane: Spotify")
            spClient = Spotify_client()
            artist = input("Specify artist name (default - Abba): ")
            if artist == "":
                artist = "Abba"
            dateRange = "1976-1979"
            tracks = spClient.get_playlists(artist=artist, date_range=dateRange)
            writeToFile = save_to_a_file()
            if writeToFile != "":
                write_dict_to_xlsx_file(tracks, ('artists', 'track name', 'release_date', 'href'), writeToFile)
        else:
            print("Nie prawidłowe dane! Nacisni 1/2/3 albo 'Q' żeby wyjsc z programu")
    exit(0)


if __name__ == "__main__":
    main()
