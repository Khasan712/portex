import os
import json
import asyncio
from django.views import View
from django.conf import settings
from django.contrib import messages
from asgiref.sync import async_to_sync
from django.shortcuts import render, redirect, reverse
from django.http import FileResponse, JsonResponse, HttpResponse

from .consumers import connected_clients
from .models import CodeBase, FeedBack
from .tasks import save_downloader


def home(request):
    return render(request, 'index.html')


def install_sh(request):
    file_path = os.path.join(settings.MEDIA_ROOT, 'install.sh')
    with open(file_path, 'r') as file:
        content = file.read()
    save_downloader.delay(request.META)
    return FileResponse(content, as_attachment=True, filename='install.sh', content_type='text/x-shellscript')


class ProxyView(View):

    @staticmethod
    def get_code_base_queryset():
        return CodeBase.objects.order_by('rank')

    def get(self, request, path):
        host = self.request.get_host()
        if host == settings.MAIN_HOST:
            meta = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = request.META.get('REMOTE_ADDR')
            print(meta, ip, '---------------11-1-11')
            context = {
                "codes": self.get_code_base_queryset()
            }
            return render(request, 'index.html', context)
        return self._proxy_request(request, path)

    def post(self, request, path):
        host = self.request.get_host()
        if host == settings.MAIN_HOST:
            text = request.POST.get('text')
            print(text)
            if text:
                FeedBack.objects.create(text=text)
                messages.success(request, 'Thanks for feedback!')
            return redirect(reverse('proxy', kwargs={'path': ''}))
        return self._proxy_request(request, path)

    def put(self, request, path):
        return self._proxy_request(request, path)

    def patch(self, request, path):
        return self._proxy_request(request, path)

    def delete(self, request, path):
        return self._proxy_request(request, path)

    def options(self, request, path):
        return self._proxy_request(request, path)

    def _proxy_request(self, request, path):
        try:
            # Extract the subdomain from the host header
            subdomain = request.headers.get("Host").split('.')[0]
            # subdomain = 'a'

            # Check if the subdomain exists in connected clients
            if subdomain not in connected_clients:
                return JsonResponse({"error": "App not found"}, status=404)

            print(f"Client exists: {subdomain}")
            print(f"Request path: {path}")
            print(f"Request method: {request.method}")

            # Get the query parameters
            params = request.GET
            print(f"Params: {params}")
            if params:
                pass

            # Get headers
            headers = dict(request.headers)
            print(f"Headers: {headers}")

            # Get the body of the request (if any)
            data = None
            if request.method in ("POST", "PUT", "PATCH"):
                if request.method == 'POST':
                    data = request.POST
                elif request.method == 'PUT':
                    data = request.PUT
                elif request.method == 'PATCH':
                    data = request.PATCH

                if data:
                    try:
                        data = dict(data)
                    except json.JSONDecodeError as e:
                        print(f"Error reading JSON body: {e}")
                print(f"Body: {data}")

            # Prepare the payload for the WebSocket
            websocket, queue = connected_clients[subdomain]
            payload = {
                "status": "send_request",
                "request": {
                    "path": path,
                    "headers": headers,
                    "body": data,
                    "params": dict(params),
                    "method": request.method
                }
            }
            print(f"Payload: {payload}")

            # Send the request to the WebSocket client
            async_to_sync(websocket.send)(json.dumps(payload))
            print("Sent request to WebSocket")

            # Wait for a response from the WebSocket
            while not queue:  # Wait until the queue is not empty
                async_to_sync(asyncio.sleep)(0.1)
            response = queue.popleft()
            response = json.loads(response)
            print(f"Response: {response}")
            content_type = response.get('content_type')
            print(f"CType: {content_type}")
            headers = response.get('headers')
            if 'content-length' in headers:
                del headers['content-length']
            if 'Content-Length' in headers:
                del headers['Content-Length']

            if content_type == 'application/json':
                return JsonResponse(
                    response.get('content'),
                    headers=headers,
                    status=response.get('status_code')
                )
            return HttpResponse(
                content=response.get('content'),
                headers=headers,
                status=response.get('status_code')
            )

        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({"error": f"Communication error: {str(e)}"}, status=500)

