from django.dispatch import receiver
from django.db.models import signals
from template.main.models import (
    BlogTitle,
    AchievementTitle,
    FirstPageContent,
    AchievementCard,
    AnswerQuestionTitle,
    ProjectTitle,
    ProductTitle,
)
from template.models import CommingSoon,LoginPage
from template.header.models import Header


@receiver(signal=signals.post_migrate)
def create_instances (sender,**kwargs) : 
    blog = BlogTitle.objects.first()

    if not blog : 
        BlogTitle.objects.create()
    
    comming_soon = CommingSoon.objects.first()

    if not comming_soon : 
        CommingSoon.objects.create()

    header = Header.objects.first()

    if not header : 
        Header.objects.create()
    
    achievements = AchievementCard.objects.first()

    if not achievements : 
        AchievementCard.objects.create()
    
    answer = AnswerQuestionTitle.objects.first()

    if not answer : 
        AnswerQuestionTitle.objects.create()

    project = ProjectTitle.objects.first()

    if not project : 
        ProjectTitle.objects.create()
    
    product = ProductTitle.objects.first()
 
    if not product : 
        ProductTitle.objects.create()
    
    first_page = FirstPageContent.objects.first()

    if not first_page : 
        FirstPageContent.objects.create()

    if not AchievementTitle.objects.first() :
        AchievementTitle.objects.first()

    if not LoginPage.objects.first() : 
        LoginPage.objects.create()