from django.dispatch import receiver
from django.db.models.signals import post_save
from ticket.models import Ticket


@receiver(post_save,sender=Ticket)
def change_state_of_ticket (sender,instance,created,**kwargs) : 
    if instance.is_from_admin and instance.reply_to : 
        try : 
            ticket = Ticket.objects.get(id=instance.reply_to.id)
            ticket.status = "responsed"
            ticket.save()
        except : 
            pass 