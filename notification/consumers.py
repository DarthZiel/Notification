import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Subscription, Notification
from datetime import datetime
from django.contrib.auth.models import User
from blog.models import Post


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            await self.accept()
            user = self.scope['user']
            authors = Subscription.objects.filter(user=user).values_list('author', flat=True)
            time_threshold = datetime.datetime.now() - datetime.timedelta(days=1)

            for author_id in authors:
                author = User.objects.get(id=author_id)
                new_posts = Post.objects.filter(owner=author, create_date__gte=time_threshold)
                for post in new_posts:
                    notification, created = Notification.objects.get_or_create(user=user)
                    if created:
                        await self.send(text_data=json.dumps({
                            'type': 'notification',
                            'message': f"Привет, у {author.username} вышел новый пост - '{post.title}', приятного чтения!!"
                        }))
        else:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        notification_id = data.get('notification_id')
        action = data.get('action')

        if notification_id and action == 'mark_as_read':
            try:
                notification = Notification.objects.get(id=notification_id, user=self.scope['user'])
                notification.is_seen = True
                notification.save()
                await self.send(text_data=json.dumps({
                    'status': 'success',
                    'message': 'Notification marked as read.'
                }))
            except Notification.DoesNotExist:
                await self.send(text_data=json.dumps({
                    'status': 'error',
                    'message': 'Notification not found.'
                }))
