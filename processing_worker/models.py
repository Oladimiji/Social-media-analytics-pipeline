from django.db import models

class SocialMediaPost(models.Model):
    user_id = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField()
    processed_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=20, default='neutral') # New field

    def _str_(self):
        return f"Post by {self.user_id} - Sentiment: {self.sentiment}"