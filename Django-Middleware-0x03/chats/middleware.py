import time
from datetime import datetime
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
import logging
from collections import defaultdict
from threading import Lock

# Setup logger to write to requests.log file
logger = logging.getLogger('request_logger')
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Thread-safe store for message timestamps by IP address
message_counts = defaultdict(list)
lock = Lock()


class RequestLoggingMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_msg = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_msg)
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access only between 6AM (6) and 9PM (21)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is restricted between 9PM and 6AM.")
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith('/api/messages/'):
            ip = self.get_client_ip(request)
            now = time.time()

            with lock:
                # Keep only timestamps within last 60 seconds
                message_counts[ip] = [t for t in message_counts[ip] if now - t < 60]

                if len(message_counts[ip]) >= 5:
                    return HttpResponseForbidden("Too many messages sent. Please wait before sending more.")

                # Record this message timestamp
                message_counts[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super().__init__(get_response)

    def __call__(self, request):
        # Restrict certain methods to admin or moderator users only
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")
            # Assumes User model has a 'role' attribute
            if getattr(user, 'role', None) not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        response = self.get_response(request)
        return response