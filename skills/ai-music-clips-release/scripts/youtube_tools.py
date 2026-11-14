#!/usr/bin/env python3
"""Share one local Google OAuth client/profile between the two creator CLIs.

Credentials and derived tokens stay outside this repository. No account changes
or API calls occur unless the user explicitly invokes connect/cli/yutu.
"""
import argparse,json,os,re,shutil,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path

CONFIG=Path(os.environ.get('XDG_CONFIG_HOME',Path.home()/'.config'))/'youtube-creator'
APP=Path(os.environ.get('YOUTUBE_CLI_APP',Path.home()/'.local/share/youtube-cli-app'))
CLIENT=CONFIG/'client_secret.json'

def secure_json(path,value):
 path.parent.mkdir(parents=True,exist_ok=True,mode=0o700);path.parent.chmod(0o700)
 fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
 with os.fdopen(fd,'w') as f:json.dump(value,f)
 path.chmod(0o600)

def client_env():
 env=os.environ.copy()
 if CLIENT.exists():
  c=json.loads(CLIENT.read_text())['installed']
  env['YOUTUBE_CLIENT_ID']=c['client_id'];env['YOUTUBE_CLIENT_SECRET']=c['client_secret']
 return env

def token_path(profile):
 return Path.home()/('.youtube-cli-token.json' if profile=='default' else f'.youtube-cli-token-{profile}.json')

def upstream(profile,args):
 cmd=[str(APP/'.venv/bin/python'),str(APP/'youtube_cli.py')]
 if profile!='default':cmd+=['--profile',profile]
 return cmd+args

def yutu_env(profile):
 if not CLIENT.exists():raise ValueError('Desktop OAuth client missing; run youtube-tools connect --client PATH')
 source=token_path(profile)
 if not source.exists():raise ValueError('This channel profile is not authorized; run youtube-tools connect --client PATH')
 t=json.loads(source.read_text());required=['https://www.googleapis.com/auth/youtube.force-ssl','https://www.googleapis.com/auth/yt-analytics.readonly']
 scopes=t.get('scopes',[])
 if any(x not in scopes for x in required):raise ValueError('The profile needs caption and analytics scopes; authorize it again')
 converted={'access_token':t.get('token',''),'token_type':'Bearer','refresh_token':t['refresh_token'],'expiry':t.get('expiry','')}
 if converted['expiry']:
  dt=datetime.fromisoformat(converted['expiry'].replace('Z','+00:00'))
  if dt.tzinfo is None:dt=dt.replace(tzinfo=timezone.utc)
  converted['expiry']=dt.astimezone(timezone.utc).isoformat().replace('+00:00','Z')
 target=CONFIG/'profiles'/profile/'youtube.token.json';secure_json(target,converted)
 env=client_env();env['YUTU_CREDENTIAL']=str(CLIENT);env['YUTU_CACHE_TOKEN']=str(target)
 return env

def main():
 os.umask(0o077)
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--profile',default=os.environ.get('YOUTUBE_PROFILE','default'))
 sub=p.add_subparsers(dest='command',required=True)
 sub.add_parser('status');c=sub.add_parser('connect');c.add_argument('--client',required=True,type=Path)
 for name in ['cli','yutu']:
  x=sub.add_parser(name,add_help=False);x.add_argument('args',nargs=argparse.REMAINDER)
 a,extra=p.parse_known_args()
 if extra:
  if a.command in ['cli','yutu']:a.args=extra+a.args
  else:p.error('Unrecognized arguments')
 if not re.fullmatch(r'[A-Za-z0-9_-]+',a.profile):p.error('Invalid profile name')
 if a.command=='status':
  print(json.dumps({'yutu_installed':bool(shutil.which('yutu')),'youtube_cli_app_installed':(APP/'youtube_cli.py').is_file(),'client_configured':CLIENT.is_file(),'profile':a.profile,'profile_token_present':token_path(a.profile).is_file()},indent=2));return
 if a.command=='connect':
  d=json.loads(a.client.expanduser().read_text());c=d.get('installed',{})
  if not c.get('client_id','').endswith('.apps.googleusercontent.com') or not c.get('client_secret'):raise ValueError('Expected a Google Desktop app OAuth client JSON file')
  for field,expected in [('auth_uri','https://accounts.google.com/o/oauth2/auth'),('token_uri','https://oauth2.googleapis.com/token')]:
   if c.get(field,expected)!=expected:raise ValueError('Unexpected OAuth service URL')
  secure_json(CLIENT,d)
  subprocess.run(upstream(a.profile,['auth']),env=client_env(),check=True)
  token_path(a.profile).chmod(0o600);yutu_env(a.profile)
  print('OAuth profile saved for both CLIs. Verify the channel ID before publishing.');return
 if not a.args:p.error('Pass a native CLI subcommand')
 if a.command=='cli':cmd=upstream(a.profile,a.args);env=client_env()
 else:cmd=['yutu']+a.args;env=yutu_env(a.profile)
 raise SystemExit(subprocess.call(cmd,env=env))

if __name__=='__main__':
 try:main()
 except (ValueError,KeyError,FileNotFoundError) as e:raise SystemExit(str(e))
