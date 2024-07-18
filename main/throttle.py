from rest_framework.throttling import UserRateThrottle

from rest_framework.exceptions import Throttled


class RoleBasedRateThrottle(UserRateThrottle):
    """
    Custom throttle class to implement role-based rate limiting.
    Differentiates between students, admins permissions.
    """

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                self.scope = "admin"
            elif request.user.is_staff:
                self.scope = "admin"
            else:
                self.scope = "student"
        else:
            self.scope = "student"

        return super().get_cache_key(request, view)

    def throttle_failure(self):
        raise Throttled(detail={"message": f"Request limit exceeded for {self.scope}"})
