from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib import messages
import uuid, string, random
# Create your models here.

class Message(models.Model):
    author = models.OneToOneField(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.content[:5]} by {self.author}'
    
    class Meta:
        permissions = [
            ('dg_delete','dg can delete message'),
        ]


class Room(models.Model):
    name = models.CharField(max_length=50)
    room_id = models.CharField(unique=True,editable=False,max_length=4)
    created_on = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='memberships')
    room_admin = models.ManyToManyField(User,)
    owner = models.ForeignKey(
        User,on_delete=models.CASCADE,
        related_name='my_rooms',related_query_name='my_rooms'
    )
    messages = models.ManyToManyField(
        Message,related_name='room', related_query_name='room'
    )

    class Meta:
        permissions = [
            ('del_room','dg can delete room'),
            ('edit_room','dg can edit message'),
            ('access_room','dg access edit message'),
            ('make_admin','dg can make admin'),
            ('remove_member','dg can remove member'),
            ('dg_requests','dg can manage requests'),
        ]
    
    def save(self,*args,**kwargs):
        self.room_id = Room.random_uuid()
        return super().save(*args,**kwargs)

    @classmethod
    def random_uuid(cls):
        id = str(uuid.uuid4())[:4].lower()
        try:
            if Room.objects.get(room_id=id).exists():    
                y = random.choice(list(string.ascii_lowercase))
                x = id[random.choice(range(0,4))]
                id = id.replace(x,y)
        except:
            pass
        return id

    def __str__(self):
        return self.name
    
    def is_owner(self,user):
        return user == self.owner
    
    def is_member(self,user):
        return user in self.members.all()
    
    def is_admin(self,user):
        return bool(
            self.is_member(user=user) and                    
            user in self.room_admin.all()
        )
    
    def make_admin(self,owner,member):
        if owner.has_perm('make_admin',self):
            room_admins = Group.objects.get(name = 'room admins')
            print('user has perm MAKE ADMIN')
            if self.is_member(user=member):
                member.groups.add(room_admins)
                self.room_admin.add(member)
            return True
        return False
    
    def revoke_admin(self,owner,admin):
        if owner.has_perm('make_admin',self):
           room_admins = Group.objects.get(name = 'room admins')
           room_admins.user_set.remove(admin)
           self.room_admin.remove(admin)
           return True
        return False
            
        
    def add_member(self,admin,user):
        if admin.has_perm('edit_room',self):
            print(f'{admin.username} has permission to add member')
            self.members.add(user)
            return True
        return False    

    def remove_member(self,admin,user):
        if admin.has_perm('edit_room',self):
            print(f'{admin.username} has permission to remove member')
            self.members.remove(user)
            return True
        return False
