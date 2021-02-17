from random import choice
from string import digits
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from account import serializers
from account.serializers import RegistrationSerializer, MyTokenObtainSerializer
from account.models import User, ActivityPeriod
from account.token import account_activation_token
import pytz
import datetime

@api_view(['POST', ])
def registration_view(request):
    user = request.data['username']
    string2 = 'W0' + ''.join(choice(digits) for i in range(7))
    randomstring = string2
    serializer = RegistrationSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        unaware = datetime.datetime(2011, 8, 15, 8, 15, 12, 0)
        now_aware = unaware.replace(tzinfo=pytz.UTC)
        account = serializer.save()
        account.username = randomstring
        account.is_active = False
        account.tz = now_aware
        account.save()
        # EMAIL VERIFICATION
        current_site = get_current_site(request)
        html_content = render_to_string('acc_active_email.html',
                                        {'user': account, 'domain': current_site.domain,
                                         'uid': urlsafe_base64_encode(force_bytes(account.pk)),
                                         'token': account_activation_token.make_token(account),
                                         })
        email = EmailMultiAlternatives('Confirm your Artomate Account')
        email.attach_alternative(html_content, "text/html")
        email.to = [request.data['email']]
        email.send()
        data['response'] = 'successfully registered new user and ' \
                           'Please confirm your email address to complete the registration '
        data['status'] = 100

    else:
        data = serializer.errors
    return Response(data)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        account = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        account = None
    if account is not None and account_activation_token.check_token(account, token):
        account.is_active = True
        account.save()
        return render(request, 'login.html')
    else:
        return HttpResponse('Activation link is invalid!')


@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_200_OK)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'kyc_message': 'kyc details not entered', 'kyc_status': 0},
                    status=HTTP_200_OK)

class TokenObtainPairPatchedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = serializers.TokenObtainPairPatchedSerializer

    token_obtain_pair = TokenObtainPairView.as_view()


class MyTokenObtain(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer


class ActivitiesView(APIView):

    def get(self, request):
        data = {}
        mylist = []
        account = User.objects.values()
        for i in account:
            activity = ActivityPeriod.objects.filter(user_id=i['id']).values('start_time', 'end_time')
            data1 = {
                "id": i['username'],
                "real_name": i['real_name'],
                "tz": i['tz'],
                "activity_periods": activity
            }
            mylist.append(data1)
        data['ok'] = True
        data['members'] = mylist
        return Response(data)

