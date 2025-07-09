from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.StartSessionAPIView.as_view(), name='start_session'),
    path('modify/', views.ModifySongAPIView.as_view(), name='modify_song'),
    path('finalize/', views.FinalizePlaylistAPIView.as_view(), name='finalize_playlist'),
    path('send-message/', views.SendMessageAPIView.as_view(), name='send_message'),
    path('sessions/', views.GetActiveSessionsAPIView.as_view(), name='get_active_sessions'),
    path('delete-session/', views.DeleteSessionAPIView.as_view(), name='delete_session'),
]