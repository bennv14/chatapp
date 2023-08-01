import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Message
from django.contrib.auth.models import User

class ChatConcsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = 'chat_' + self.room_name
        print(self.room_name, self.room_group_name)
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        
        self.accept()
        
        self.send(text_data=json.dumps({
            'type': 'connection_established',
            'messages': 'welcome to group chat ' + self.room_group_name 
        }))
        
    
    def receive(self, text_data):
        json_data = json.loads(text_data)
        print('Message:',json_data)
        
        if json_data['type'] == 'new_message':
            message = json_data['message']
            username = json_data['username']
            sender = User.objects.get(username=username)
            chat = Chat.objects.get(id=self.room_name)
            Message.objects.create(message=message, sender = sender, chat=chat).save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'new_message',
                    'username':username,
                    'message': message
                }
            )
        elif json_data['type'] == 'all_messages':
            messages = Message.objects.filter(chat_id=self.room_name).order_by('time_send')
            list_messages = []
            for message in messages:
                dict_message = {
                    'id':message.id,
                    'chat_id':message.chat.id,
                    'sender_name':message.sender.username,
                    'message':message.message,
                    'time_send':message.time_send.strftime("%m/%d/%Y, %H:%M:%S")
                }
                list_messages.append(dict_message)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'all_messages',
                    'messages': list_messages
                }
            )
            
    def new_message(self, event):
        message = event['message']
        username = event['username']
        self.send(text_data=json.dumps({
            'type':'new_message',
            'username':username,
            'message':message
        }))
        
    def all_messages(self, event):
        print('send')
        messages = event['messages']
        self.send(text_data=json.dumps({
            'type':'all_messages',
            'messages':messages
        }))
        