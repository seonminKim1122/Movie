from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Platform, Party
from .serializers import PlatformListSerializer, PartyCreateSerializer, PartyListSerializer, PartyModifySerializer

from accounts.utils import validate_token

# Create your views here.
@api_view(['GET'])
def all_platforms(request):
    platforms = Platform.objects.all()
    serializer = PlatformListSerializer(instance=platforms, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST', 'GET'])
def parties(request):

    result = validate_token(request)
    if request.method == 'POST':
        if not result[0]: return result[1]

        user = request.user
        if not Platform.objects.filter(id=request.data.get('platform')).exists():
            return Response({"message": "Invalid Platform Id"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        platform = Platform.objects.get(id=request.data.get('platform'))
        serializer = PartyCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            party = serializer.save(owner=user, platform=platform)
            party.participants.add(user)
            party.save()
            return Response({"partyId": party.id},
                            status=status.HTTP_200_OK) 

    elif request.method == 'GET':
        if not result[0]:
            user = None
        else:
            user = result[1]

        try:
            platform_info = request.GET.get('platforms')
            platform_ids =list(map(int, platform_info.replace(' ', '').split(',')))
            party_list = Party.objects.filter(platform__id__in=platform_ids).exclude(participants=user)
            serializer = PartyListSerializer(party_list, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except:
            party_list = Party.objects.exclude(participants=user)
            serializer = PartyListSerializer(party_list, many=True)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        


@api_view(['POST'])
def join_party(request, party_id):
    result = validate_token(request)
    if not result[0]:return result[1]
    
    if not Party.objects.filter(id=party_id).exists():
        return Response({"message": "Not exists"},
                        status=status.HTTP_404_NOT_FOUND)
    
    user = request.user
    party = Party.objects.get(id=party_id)
    if party.participants.contains(user):
        return Response({"message": "Already joined"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if party.capacity <= len(party.participants.all()):
        return Response({"message": "Already full"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    party.participants.add(user)

    return Response({"message": "Success"}, status=status.HTTP_200_OK)
    


@api_view(['DELETE'])
def withdraw_party(request, party_id):
    result = validate_token(request)
    if not result[0]:return result[1]

    if not Party.objects.filter(id=party_id).exists():
        return Response({"message": "Not exists"},
                        status=status.HTTP_404_NOT_FOUND)
    
    party = Party.objects.get(id=party_id)
    user = request.user

    # 본인이 만든 파티인 경우 탈퇴 불가능
    if party.owner == user:
        return Response({"message": "Can't leave party you've created"},
                        status=status.HTTP_400_BAD_REQUEST)

    if not party.participants.contains(user):
        return Response({"message": "Can't find participation info"},
                        status=status.HTTP_400_BAD_REQUEST)
    
    party.participants.remove(user)

    return Response({"message":"Success"},
                    status=status.HTTP_200_OK)



@api_view(['PUT'])
def party(request, party_id):
    result = validate_token(request)
    if not result[0]:return result[1]

    if not Party.objects.filter(id=party_id).exists():
        return Response({"message": "Can't find party"},
                        status=status.HTTP_404_NOT_FOUND)
    
    party = Party.objects.get(id=party_id)
    user = request.user

    if not party.owner == user:
        return Response({"message": "Only party owner can modify infos"},
                        status=status.HTTP_403_FORBIDDEN)
    
    serializer = PartyModifySerializer(instance=party, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({"message": "Success"}, status=status.HTTP_200_OK)