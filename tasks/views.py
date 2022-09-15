from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .serializers import TaskSerializer
from .models import Task


@csrf_exempt
def tasks(request):
    # List all task snippets
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # save it on the database
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except:
        return HttpResponse(status=404)
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=204)  # return a no content response
