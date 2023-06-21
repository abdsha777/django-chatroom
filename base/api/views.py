from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(["GET"])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)

@api_view(['GET'])
def getRooms(requests):
    rooms = Room.objects.all()
    ser = RoomSerializer(rooms,many=True)
    return Response(ser.data)

@api_view(['GET'])
def getRoom(requests,pk):
    rooms = Room.objects.get(id=pk)
    ser = RoomSerializer(rooms,many=False)
    return Response(ser.data)

