import re
from django.http import FileResponse, HttpResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
import os

class RangeFileWrapper(FileWrapper):
    def __init__(self, filelike, blksize=8192, offset=0, length=None):
        self.filelike = filelike
        self.blksize = blksize
        self.offset = offset
        self.length = length

    def __iter__(self):
        with self.filelike:
            self.filelike.seek(self.offset, os.SEEK_SET)
            remaining = self.length
            while remaining > 0:
                read_length = min(self.blksize, remaining)
                data = self.filelike.read(read_length)
                if not data:
                    break
                remaining -= len(data)
                yield data

class RangeRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'HTTP_RANGE' in request.META:
            response = self.process_range_request(request, response)
        return response

    def process_range_request(self, request, response):
        range_header = request.META.get('HTTP_RANGE', '').strip()
        range_match = re.match(r'bytes=(\d+)-(\d+)?', range_header)
        if range_match:
            first_byte, last_byte = range_match.groups()
            first_byte = int(first_byte)
            last_byte = int(last_byte) if last_byte else None

            file_size = os.path.getsize(response.file_to_stream.path)
            if last_byte is None or last_byte >= file_size:
                last_byte = file_size - 1
            length = last_byte - first_byte + 1

            response = HttpResponse(
                RangeFileWrapper(response.file_to_stream.file, offset=first_byte, length=length),
                status=206,
                content_type=response['Content-Type']
            )
            response['Content-Length'] = str(length)
            response['Content-Range'] = 'bytes %s-%s/%s' % (first_byte, last_byte, file_size)
        return response