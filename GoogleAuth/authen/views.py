import httplib2
from googleapiclient.discovery import build
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from .models import CredentialsModel
from GoogleAuth import settings
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from django.shortcuts import render
from httplib2 import Http

def home(request):
    status = True

    if not request.user.is_authenticated:
        return HttpResponseRedirect('admin')

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    try:
        access_token = credential.access_token
        resp, cont = Http().request("https://www.googleapis.com/auth/gmail.readonly",
                                    headers={'Host': 'www.googleapis.com',
                                            'Authorization': access_token})
    except:
        status = False
        print('Not Found')

    return render(request, 'index.html', {'status': status})


################################
#   GMAIL API IMPLEMENTATION   #
################################

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>


from google_auth_oauthlib.flow import Flow

# Load the client secrets file
client_secrets_file = "D:\PYTHON\Django_Tutorial\Google authentication\GoogleAuth\client.json"

# Use the client secrets file to start a Flow object and initiate an OAuth 2.0 flow
flow = Flow.from_client_secrets_file(
    client_secrets_file,
    scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'],
    redirect_uri='http://localhost:8000/oauth2callback')


def gmail_authenticate(request):
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    credential = storage.get()
    if credential is None or credential.invalid:
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                       request.user)
        authorize_url = FLOW.step1_get_authorize_url()
        return HttpResponseRedirect(authorize_url)
    else:
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build('gmail', 'v1', http=http)
        print('access_token = ', credential.access_token)
        status = True

        return render(request, 'index.html', {'status': status})


def auth_return(request):
    get_state = bytes(request.GET.get('state'), 'utf8')
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state,
                                   request.user):
        return HttpResponseBadRequest()
    credential = FLOW.step2_exchange(request.GET.get('code'))
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
    storage.put(credential)
    print("access_token: %s" % credential.access_token)
    return HttpResponseRedirect("/")