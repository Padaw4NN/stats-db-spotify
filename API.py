import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class API:
    def __init__(self, client_id=None, client_secret=None, scope=None, redirect_uri=None):
        self.scope        = scope
        self.client_id    = client_id
        self.client_sec   = client_secret
        self.redirect_uri = redirect_uri

    def auth(self):
        """
        função de autorização para o
        acesso  à  API  do   Spotify
        """
        auth__ = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_sec, 
            redirect_uri=self.redirect_uri,
            scope=self.scope
        )
        return spotipy.Spotify(auth_manager=auth__)


    def save_json(self, data:list) -> json:
        """
        função   para  salvar
        os dados em   formato
        json para importar no
        NoSQL         MongoDB
        """
        dict_to_json_data = {
            "data": {
                "names": [
                    {
                        "alexander": {
                            "artists": data[0],
                            "tracks":  data[2],
                            "genres":  data[1],
                            "albums":  data[3]
                        }
                    }
                ]
            }
        }

        # salva o json usando a library do proprio python
        with open("exported_json_data.json", 'w') as json_file:
            json_file.write(json.dumps(dict_to_json_data))


    def run(self):
        """
        função para a extração dos dados
        através   dos  objetos  da   API

        data[0]: top artists
        data[1]: top  genres
        data[2]: top  tracks
        data[3]: top  albuns

        [!!] PELA  FALTA DE  DADOS DA CONTA
        ...  O  LOOP  FOI  REDUZIDO PARA  3
        ...  INDICIES   PARA    EVITAR    O
        ...  EXCEPTION "INDEX OUT OF RANGE"

        return:
        lista de listas, onde cada lista
        é  cada  dado  extraído  da  API
        """

        # objeto da API criado
        api = self.auth()
        os.system("clear")

        # pega o nome do dono da conta do Spotify
        current_user_ = api.current_user()
        current_user_ = current_user_["display_name"]
        print(f"\n[*] Running: {current_user_[0:9]} inf")
        print()


        # lista vazia para inserção de cada dado
        data = []


        # busca os artistas mais ouvidos da conta
        # insere na lista de dados
        artists = []
        artists_rs = api.current_user_top_artists()
        for i in range(len(artists_rs["items"])):
            artists.append(artists_rs["items"][i]["name"])
            if i == 2:
                break
        data.append(artists)


        # busca os gêneros mais escutados da conta
        # insere na lista de dados
        genres = []
        artists_rs = api.current_user_top_artists()
        for i in range(len(artists_rs["items"])):
            genres.append(artists_rs["items"][i]["genres"])
            if i == 2:
                break
        data.append(genres)


        # busca as musicas  mais escutadas
        # através do ID retirado do objeto
        # de   artistas   mais   escutados
        # insere na lista de dados
        tracks = []
        artist_track_id = artists_rs["items"][0]["id"]
        tracks_rs = api.artist_top_tracks(artist_id=artist_track_id)
        for i in range(len(tracks_rs["tracks"])):
            tracks.append(tracks_rs["tracks"][i]["name"])
            if i == 2:
                break
        data.append(tracks)


        # busca  os  albuns  mais escutados
        # através do ID do artista extraído
        # dos   artistas   mais   escutados
        # insere na lista de dados
        albums = []
        albums_rs = api.artist_top_tracks(artist_id=artist_track_id)
        for i in range(len(albums_rs["tracks"])):
            albums.append(albums_rs["tracks"][i]["album"]["name"])
            if i == 2:
                break
        data.append(albums)

        # retorno da matriz de dados
        # que  será  indexado para a
        # criação  do  arquivo  json
        return data

