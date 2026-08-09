"""
Ejecútalo UNA sola vez EN LOCAL para obtener tu YT_REFRESH_TOKEN.
(Alternativa sin Python: usar Google OAuth Playground — ver README.)

Requisitos:
  pip install google-auth-oauthlib
  Descarga client_secret.json desde Google Cloud (credencial OAuth) y ponlo aquí al lado.

Uso:
  python auth_youtube.py
Se abrirá el navegador; autoriza con la cuenta del canal. Al final imprime el
refresh token: cópialo a la secret YT_REFRESH_TOKEN de GitHub.
"""
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
    print("\n================ COPIA ESTO ================")
    print("YT_CLIENT_ID     =", creds.client_id)
    print("YT_CLIENT_SECRET =", creds.client_secret)
    print("YT_REFRESH_TOKEN =", creds.refresh_token)
    print("===========================================")
    if not creds.refresh_token:
        print("\n[!] No llegó refresh_token. Revoca el acceso en tu cuenta Google "
              "y repite (hace falta 'prompt=consent' + 'access_type=offline').")


if __name__ == "__main__":
    main()
