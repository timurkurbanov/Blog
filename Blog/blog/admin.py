from django.contrib import admin
from blog.models import Article, Comment, Topic

# registering Article with the admin back-end
admin.site.register(Article)
# registering Comment with the admin back-end
admin.site.register(Comment)
# registering Topic with the admin back-end
admin.site.register(Topic)
