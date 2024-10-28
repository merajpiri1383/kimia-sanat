from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from ticket.models import Ticket
from ticket.tasks import (
    send_user_ticket_responsed,
    send_user_ticket_is_sent,
    send_admin_user_send_ticket
)


@receiver(post_save,sender=Ticket)
def change_state_of_ticket (sender,instance,created,**kwargs) : 
    if instance.is_from_admin and instance.reply_to : 
        try : 
            ticket = Ticket.objects.get(id=instance.reply_to.id)
            ticket.status = "responsed"
            ticket.save()
            send_user_ticket_responsed.apply_async(args=[
                ticket.user.username(),
                ticket.user.phone,
                ticket.number
            ])
        except : 
            pass 
    if created and not instance.is_from_admin :
        try : 
            send_user_ticket_is_sent.apply_async(args=[
                instance.user.username(),
                instance.user.phone,
                instance.number  
            ])
        
            for user in get_user_model().objects.filter(is_staff=True,send_sms=True) : 
                send_admin_user_send_ticket.apply_async(args=[
                    instance.number,
                    instance.user.username(),
                    user.phone
                ])
        except : 
            pass 