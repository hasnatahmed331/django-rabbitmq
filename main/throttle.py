from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled


class RoleBasedRateThrottle(UserRateThrottle):
    """
    Custom throttle class to implement role-based rate limiting.
    Differentiates between students and admins permissions.
    """

    def get_cache_key(self, request, view):
        """
        Returns a unique cache key for the request to enforce rate limits.

        Args:
            request (Request): The current request object.
            view (View): The view being accessed.

        Returns:
            str: The cache key to be used for throttling.
        """
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # If the user is a superuser or staff, set the scope to 'admin'
            if request.user.is_superuser:
                self.scope = "admin"
            elif request.user.is_staff:
                self.scope = "admin"
            else:
                # Otherwise, set the scope to 'student'
                self.scope = "student"
        else:
            # If the user is not authenticated, set the scope to 'student'
            self.scope = "student"

        # Call the parent class's get_cache_key method with the updated scope
        return super().get_cache_key(request, view)

    def throttle_failure(self):
        """
        Custom behavior when the rate limit is exceeded.

        Raises:
            Throttled: Exception indicating the request limit has been exceeded.
        """
        # Raise a Throttled exception with a custom message indicating which scope's limit was exceeded
        raise Throttled(detail={"message": f"Request limit exceeded for {self.scope}"})
