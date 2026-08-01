def main() -> None:
    try:
        client_id, client_secret = load_credentials()
        access_token = get_access_token(client_id, client_secret)

        lunaria = get_coalition_by_id(access_token, 459)
        print(lunaria)

    except requests.Timeout:
        print("Przekroczono czas oczekiwania na odpowiedź 42 API.")
        sys.exit(1)

    except requests.HTTPError as error:
        response = error.response

        if response is None:
            print(f"Wystąpił błąd HTTP: {error}")
        else:
            print(f"42 API zwróciło HTTP {response.status_code}.")
            print(response.text)

        sys.exit(1)

    except requests.RequestException as error:
        print(f"Błąd połączenia z 42 API: {error}")
        sys.exit(1)

    except (RuntimeError, ValueError) as error:
        print(f"Błąd konfiguracji lub danych: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()