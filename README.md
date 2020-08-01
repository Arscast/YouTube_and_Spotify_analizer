# YouTube_and_Spotify_analizer

Aplikacja ma pobierać listę utworów (filmów lub podcastów) z Youtube i
spotify oraz możliwość wyeksportowania tej listy do pliku excell.

Pobierane informacje: twórca, tytuł , datat dodania, hashtagi (jeśli są), link

## Sposób działania

Po uruchomieniu aplikacji :

Wybierz źródło : YT/spotify
Podaj nazwę konta z którego pobrać dane
Podaj datę od której mają być pobrane dane
Aplikacja wyświetla listę pobranych informacji.
Pytanie : czy zapisać do pliku xls (jeśli tak podaj nazwę pliku)

## Jak uruchomić

```bash
# konfiguracja i aktywacja venev
pip install --upgrade google-api-python-client google_auth_oauthlib spotipy openpyxl python-dateutil flake8

# ustawienie zmiennych env:

export SPOTIPY_CLIENT_ID=client_id_here
export SPOTIPY_CLIENT_SECRET=client_secret_here

#w systemie Windows użyj `SET` zamiast `export`
```

## CO TRZEBA ZROBIĆ

- obsługa większej liczby wyjątków
- badania jednostkowe
- dodać kompozytora do wyświetlenia na wyjściu
- analiza składniowa  parametrów z  dopomogą argparse (opcjonalne)

## Strony internetowe

<https://developers.google.com/youtube/v3/guides/working_with_channel_ids>
<https://github.com/youtube/api-samples>
<https://github.com/plamere/spotipy>

