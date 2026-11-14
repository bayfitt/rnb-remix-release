#!/usr/bin/env python3
"""One-time OAuth using an available loopback port and the upstream app's scopes."""
import argparse,json,os,runpy
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
p=argparse.ArgumentParser();p.add_argument('--client',type=Path,required=True);p.add_argument('--token',type=Path,required=True);p.add_argument('--app',type=Path,required=True);a=p.parse_args()
os.umask(0o077)
upstream=runpy.run_path(str(a.app/'youtube_cli.py'),run_name='youtube_cli_config')
flow=InstalledAppFlow.from_client_secrets_file(str(a.client),scopes=upstream['SCOPES'])
creds=flow.run_local_server(host='localhost',port=0,open_browser=True,prompt='consent',timeout_seconds=300,authorization_prompt_message='Google authorization page opened; waiting for the authorized account.',success_message='YouTube CLI connected. You may close this tab.')
fd=os.open(a.token,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
with os.fdopen(fd,'w') as f:f.write(creds.to_json())
a.token.chmod(0o600)
print('Google OAuth token saved privately.')
