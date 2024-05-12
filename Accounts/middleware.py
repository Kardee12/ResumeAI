# from django.shortcuts import redirect
# from django.urls import resolve
#
# class SetupMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         response = self.get_response(request)
#         if request.user.is_authenticated and not request.user.has_completed_setup:
#             current_url = resolve(request.path_info).url_name
#             if current_url not in ['setup', 'logout']: #add urls that should be accessible without redirection
#                 ##basically if url not one of these then it will redirect if setup url not done
#                 return redirect('setup_url')  # Adjust 'setup_url' to your setup page's URL name
#         return response
