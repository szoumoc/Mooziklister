from allauth.socialaccount.models import SocialToken
from django.http import HttpResponse

def your_view(request):
    if not request.user.is_authenticated:
        return HttpResponse("Please log in first")
    
    try:
        # Get the stored Spotify token
        social_token = SocialToken.objects.get(
            account__user=request.user,
            account__provider='spotify'
        )
        
        access_token = social_token.token
        refresh_token = social_token.token_secret  # For refreshing when expired
        
        return HttpResponse(f"""
            <h2>Your Spotify Tokens:</h2>
            <p><strong>Access Token:</strong> {access_token}</p>
            <p><strong>Refresh Token:</strong> {refresh_token}</p>
            <p><strong>Expires:</strong> {social_token.expires_at}</p>
        """)
        
    except SocialToken.DoesNotExist:
        return HttpResponse("No Spotify token found. Please connect your Spotify account.")