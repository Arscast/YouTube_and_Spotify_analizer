# replace with your values
export SPOTIPY_CLIENT_ID=client_id_here
export SPOTIPY_CLIENT_SECRET=client_secret_here
export DEVELOPER_KEY=api_key_here

FILE=client_secret.json

if [ ! -f "$FILE" ]; then
    echo "Environment not configured properly."
    echo "$FILE not exists."
    exit 1
fi

if [ "$SPOTIPY_CLIENT_ID" == "client_id_here" ]; then
  echo "1"
fi

python main.py
