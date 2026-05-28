from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import AirUnit, Zone, Air
from .serializers import AirUnitSerializer, ZoneSerializer, AirSerializer
from hvac.utils import session
import json

class AirUnitValuesView(APIView):
    def get(self, request, session_id):
        airunit = AirUnit.objects.filter(session_id=session_id)
        serializer = AirUnitSerializer(airunit, many=True)
        return Response(serializer.data)
    
    def post(self, request, session_id):
        airunit = AirUnit.objects.filter(session_id=session_id)
        serializer = AirUnitSerializer(airunit, data=request.data, partial=True)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class ZoneValuesView(APIView):
    def get(self, request, session_id, pk):
        zones = Zone.objects.filter(session_id=session_id).all()
        zone = zones.get(pk=pk)
        serializer = ZoneSerializer(zone)
        return Response(serializer.data)
    
    def post(self, request, session_id, pk):
        zones = Zone.objects.filter(session_id=session_id).all()
        zone = zones.get(pk=pk)
        serializer = ZoneSerializer(zone, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class AllZoneValuesView(APIView):
    def get(self, request, session_id):
        zones = Zone.objects.filter(session_id=session_id).all()
        serializer = ZoneSerializer(zones, many=True)
        return Response(serializer.data)
    
class AirValuesView(APIView):
    def get(self, request, session_id):
        air = Air.objects.filter(session_id=session_id)
        serializer = AirSerializer(air, many=False)
        return Response(serializer.data)
    
    def post(self, request, session_id):
        air = Air.objects.filter(session_id=session_id)
        serializer = AirSerializer(air, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
@method_decorator(csrf_exempt, name='dispatch')
class CreateView(View):
    async def get(self, request):
        session_id = request.GET.get('session_id')
        if session_id is None:
            sessions = [s.to_dict() for s in session.manager.active_sessions.values()]
            return JsonResponse({"sessions": sessions})
        s = session.manager.active_sessions.get(int(session_id))
        if s is None:
            return JsonResponse({'error': 'session not found'}, status=404)
        return JsonResponse(s.to_dict())

    async def post(self, request):
        body = json.loads(request.body)
        session_type = body.get('session-type')
        if session_type == 'new':
            s = session.manager.new_session()
            return JsonResponse(s.to_dict())
        return JsonResponse({'error': 'invalid session-type'}, status=400)