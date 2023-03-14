from django.db import models
from django.contrib.auth.models import User, Group, Permission
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
    room_id = models.CharField(unique=True,max_length=4,blank=True,null=False)
    created_on = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='memberships', blank=True)
    requests = models.ManyToManyField(User, related_name='requests', blank=True)
    room_admin = models.ManyToManyField(User, blank=True, related_name='administrations')
    owner = models.ForeignKey(
        User,on_delete=models.CASCADE, blank=True,
        related_name='my_rooms',related_query_name='my_rooms'
    )
    messages = models.ManyToManyField(
        Message,related_name='room', related_query_name='room',
        blank=True
    )

    class Meta:
        ordering =['name']
    
    def save(self,*args,**kwargs):
        if self.room_id == '':
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
    
    def admit_user(self,user):
        if not self.is_member(user):
            if user in self.requests.all():
                return 'request pending'
            self.requests.add(user)
            return 'private room!, request sent'
        return True
    
    def approve_requests(self,admin,user):
        if admin.has_perm('change_room',self):
            self.members.add(user)
            return True
        return False    
    
    def decline_requests(self,admin,user):
        if admin.has_perm('change_room',self):
            self.requests.remove(user)
            return True
        return False    

    def remove_member(self,admin,user):
        if admin.has_perm('change_room',self):
            print(f'{admin.username} has permission to remove member')
            self.members.remove(user)
            return True
        return False
    
    def make_admin(self,owner,member):
        if self.is_owner(user=owner):
            room_admins = Group.objects.get(name = 'room admins')
            print('user has perm MAKE ADMIN')
            if self.is_member(user=member):
                member.groups.add(room_admins)
                self.room_admin.add(member)
                return True
        return False
    
    def revoke_admin(self,owner,admin):
        if self.is_owner(user=owner):
           room_admins = Group.objects.get(name = 'room admins')
           room_admins.user_set.remove(admin)
           self.room_admin.remove(admin)
           return True
        return False
            
        
    