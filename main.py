from API import API

def main():
    sp_api = API(
        client_id="__client_id_here__",
        client_secret="__client_secret_here__",
        scope="user-top-read",                              # definição de nível de acesso
        redirect_uri="http://localhost"
    )

    # extração dos dados
    resp = sp_api.run()

    # criação do arquivo json
    sp_api.save_json(resp)


if __name__ == "__main__":
    main()
    print("\nSAVED JSON FILE\n\n")
