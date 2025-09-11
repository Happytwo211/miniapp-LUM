from .models import Story

def stories_processor(request):
    """
    Добавляет активные истории (stories) в контекст шаблонов.
    """
    return {
        'stories': Story.objects.filter(is_active=True)
    }
