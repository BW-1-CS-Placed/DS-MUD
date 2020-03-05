from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
# from pusher import Pusher
from django.http import JsonResponse
from decouple import config
from django.contrib.auth.models import User
from .models import *
from rest_framework.decorators import api_view
import json

# instantiate pusher
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))


@csrf_exempt
@api_view(["GET"])
def initialize(request):
    user = request.user
    player = user.player
    player_id = player.id
    uuid = player.uuid
    room = player.room()
    players = room.player_names(player_id)

    return JsonResponse({'uuid': uuid, 'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players}, safe=True)


# @csrf_exempt
@api_view(["POST"])
def move(request):
    dirs = {"n": "north", "s": "south", "e": "east", "w": "west"}
    reverse_dirs = {"n": "south", "s": "north", "e": "west", "w": "east"}
    player = request.user.player
    player_id = player.id
    player_uuid = player.uuid
    data = json.loads(request.body)
    direction = data['direction']
    room = player.room()
    next_room_id = None

    if direction == "n":
        next_room_id = room.n_to
    elif direction == "s":
        next_room_id = room.s_to
    elif direction == "e":
        next_room_id = room.e_to
    elif direction == "w":
        next_room_id = room.w_to

    if next_room_id is not None and next_room_id > 0:
        next_room = Room.objects.get(id=next_room_id)

        player.current_room = next_room_id
        player.save()

        players = next_room.player_names(player_id)
        current_player_uuids = room.player_uuids(player_id)
        next_players_uuids = next_room.player_uuids(player_id)

        # for p_uuid in currentPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has walked {dirs[direction]}.'})
        # for p_uuid in nextPlayerUUIDs:
        #     pusher.trigger(f'p-channel-{p_uuid}', u'broadcast', {'message':f'{player.user.username} has entered from the {reverse_dirs[direction]}.'})

        return JsonResponse({'name': player.user.username, 'title': next_room.title, 'description': next_room.description, 'players': players, 'error_msg': ""}, safe=True)

    else:
        players = room.player_names(player_id)

        return JsonResponse({'name': player.user.username, 'title': room.title, 'description': room.description, 'players': players, 'error_msg': "You cannot move that way."}, safe=True)


@csrf_exempt
@api_view(["POST"])
def say(request):
    # IMPLEMENT
    return JsonResponse({'ERROR': "Not Yet Implemented"}, safe=True, status=500)


@csrf_exempt
@api_view(["GET"])
def rooms(request):
    room_objects = Room.objects.all()
    rooms_list = []

    for i in range(len(room_objects)):
        rooms_list.append({
            'id': room_objects[i].id,
            'title': room_objects[i].title
        })

    return JsonResponse({'rooms': rooms_list}, safe=True)
