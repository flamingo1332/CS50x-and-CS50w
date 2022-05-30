from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")

    # liker = ArrayField(models.CharField(max_length=150), default=list)
    # like 모델 새로 만들었다가 HTML template에 like 수 표시하는거 너무 어려워서 arrayfield 만듬.
    # 어려워진 이유는 intfield 안써서(like 아이디마다 중복 안되게 하려고) 
    # 만들었는데 sqlite3에는 arrayfield 못씀
    liker = models.ManyToManyField(User, related_name='like_post')
    # manytomanyfield 사용하면 편하다. 이거 몰라서 개고생함
    # 그다음엔 javascript API 사용해서 manytomanyfield 값 수정(append)하는 방법 사용할려 했는데
    # 어떻게하는지 찾아도 안나온다.. mail에서 했듯이 archive:true 이렇게 간단하게 되지 않는다.
    # 결국 javascript 못씀

    content = models.TextField(max_length=256)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"id :{self.id}, liker: {self.liker}, username:{self.username}, content:{self.content}, datetime:{self.date}"

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    followedby = models.CharField(max_length=128)
    followingto = models.CharField(max_length=128)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"id:{self.id}, followedby :{self.followedby}, followingto:{self.followingto}, datetime:{self.date}"

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commented_post", null=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    content = models.TextField(max_length=256)
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"id :{self.id}, post.id: {self.Post.id} username:{self.username}, content:{self.content}, datetime:{self.date}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liker")
    date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"post_id:{self.Post_id} username:{self.username}, datetime:{self.date}"
