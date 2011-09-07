class UserProfileMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated():
            request.user_profile = None
            try:
                p = request.user.get_profile()
                request.user_profile = p.profile
            except:
                pass
