from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication as BaseJWTAuthentication


class JWTAuthentication(BaseJWTAuthentication):
    def authenticate(self, request):
        view = request.resolver_match.func.cls
        permission_classes = getattr(view, 'permission_classes', [])
        
        if IsAuthenticated not in permission_classes:
            return None
        
        return super().authenticate(request)
