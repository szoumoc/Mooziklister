from django.shortcuts import render
from rest_framework import serializers, views, status, permissions
from rest_framework.response import Response
import google.generativeai as genai
import uuid
import os
from dotenv import load_dotenv
from .serializers import (
    StartSessionSerializer,
    ModifySongSerializer,
    FinalizePlaylistSerializer,
    SendMessageSerializer,
    DeleteSessionSerializer
)


# User Journey:

# Start: "Generate 10 romantic jazz songs"
# Modify: User clicks "Edit" on Song #3 → Uses ModifyAPI
# General Chat: "Make everything more upbeat" → Uses SendMessageAPI
# Specific Edit: Changes Song #7's tempo → Uses ModifyAPI
# Finalize: "Generate now" → FinalizeAPI








# Configure your Gemini API key
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Load the Gemini model
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# Store chat sessions in memory (in production, use cache or database)
chat_sessions = {}

# Define your custom system context
SYSTEM_CONTEXT = """<s>
You are an AI **Song Generation Agent**. Your job is to generate songs based on user input (like theme, genre and if they dont specify then find a mix of trendy and classic songs),
and improve them based on structured feedback. You work in a loop until the user finalizes the playlist.
if you are asked to do anything outside songs you simply return "I am unauthorised to perform this specific task"

Your Responsibilities:
Generate the number of songs (or 15 songs if there is no specific number) unique songs when the user gives an initial prompt.

Wait for feedback – the user might ask to modify, regenerate, or accept specific songs.
Use this feedback to improve the selected songs and Maintain the others or you can also be asked to modify the whole playlist but keeping the number of songs same 
Repeat until the user says: "generate now" – then finalize the playlist.

Format: Each song should have: Title, singer stored in a dictionary and nothing else no extra words just the dictionary
example format: {'Name': ['Money trees', 'Good Morning', 'Beat It'],
                  'Singer':['Kendrik Lamar','Kanye West','Michael Jackson']}

Feedback Loop: All feedback will come as true or false value from function calls (e.g., for song id 1, flase or regenerate or delete or maybe a prompt from the user)
Don't lose track of which songs were modified.
Try to learn the user's style over multiple rounds.
</s>

<Example User Flow>   { name : song, singer
User: "Make 20 songs about heartbreak in Lo-Fi style"
Agent: (generates songs 1–10)
User: modifysong(5)
User: modifysong(9)
Agent: (generates modifications along with last generations)
User: "Make these in Jazz style"
Agent: (generates songs 1–10 again as asked by the user)
User: "generate now"
Agent: (Finalizes and outputs accepted + modified versions)
</Example User Flow>"""

class StartSessionAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = StartSessionSerializer(data=request.data)
            if serializer.is_valid():
                # Generate session ID
                session_id = str(uuid.uuid4())
                
                # Start chat with system context
                chat = model.start_chat(history=[
                    {"role": "user", "parts": [SYSTEM_CONTEXT]}
                ])
                
                # Store session
                chat_sessions[session_id] = chat
                
                # Send initial prompt
                response = chat.send_message(serializer.validated_data['prompt'])
                
                return Response({
                    'session_id': session_id,
                    'response': response.text,
                    'status': 'success'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# ModifySongAPIView - Structured Song Editing
# Purpose: Precise, structured modifications to specific songs
# Use Cases:

# User wants to change a specific song's mood: modify_song(song_id=3, mood="hopeful")
# User wants to change genre: modify_song(song_id=7, genre="blues")
# User wants to keep lyrics but change style: modify_song(song_id=5, keep_lyrics=True, change_genre="rock")







class ModifySongAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = ModifySongSerializer(data=request.data)
            if serializer.is_valid():
                session_id = serializer.validated_data['session_id']
                modification = serializer.validated_data['modification']
                
                if session_id not in chat_sessions:
                    return Response(
                        {'error': 'Invalid session_id'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                chat = chat_sessions[session_id]
                
                # Send modification request
                response = chat.send_message(modification)
                
                return Response({
                    'session_id': session_id,
                    'response': response.text,
                    'status': 'modified'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class FinalizePlaylistAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = FinalizePlaylistSerializer(data=request.data)
            if serializer.is_valid():
                session_id = serializer.validated_data['session_id']
                
                if session_id not in chat_sessions:
                    return Response(
                        {'error': 'Invalid session_id'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                chat = chat_sessions[session_id]
                
                # Send finalize command
                response = chat.send_message("generate now")
                
                # Clean up session after finalization
                del chat_sessions[session_id]
                
                return Response({
                    'session_id': session_id,
                    'final_playlist': response.text,
                    'status': 'finalized'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# SendMessageAPIView - Natural Conversation
# Purpose: Open-ended, conversational interaction with the AI
# Use Cases:

# "Can you make all the songs more upbeat?"
# "I don't like the current vibe, make it more romantic"
# "Add more instrumental songs to the mix"
# "The lyrics are too sad, can you brighten them up?"



class SendMessageAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = SendMessageSerializer(data=request.data)
            if serializer.is_valid():
                session_id = serializer.validated_data['session_id']
                message = serializer.validated_data['message']
                
                if session_id not in chat_sessions:
                    return Response(
                        {'error': 'Invalid session_id'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                chat = chat_sessions[session_id]
                
                # Send message
                response = chat.send_message(message)
                
                return Response({
                    'session_id': session_id,
                    'response': response.text,
                    'status': 'success'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class GetActiveSessionsAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            active_sessions = list(chat_sessions.keys())
            return Response({
                'active_sessions': active_sessions,
                'count': len(active_sessions)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeleteSessionAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        try:
            serializer = DeleteSessionSerializer(data=request.data)
            if serializer.is_valid():
                session_id = serializer.validated_data['session_id']
                
                if session_id not in chat_sessions:
                    return Response(
                        {'error': 'Invalid session_id'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                del chat_sessions[session_id]
                
                return Response({
                    'message': f'Session {session_id} deleted successfully'
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )