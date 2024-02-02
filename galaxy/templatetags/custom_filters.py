from django import template
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib.sessions.backends.db import SessionStore

register = template.Library()

@register.filter(name='active_sessions')
def active_sessions(user_id):

    session_model = Session.objects.using('app').filter(expire_date__gte=timezone.now())
    the_user_sessions = []

    for session in session_model:
        session_data = session.get_decoded()
        if 'user_id' in session_data and session_data['user_id'] == user_id:
            session_store = SessionStore(session_key=session.session_key)
            the_user_sessions.append(session_store)
    
    if the_user_sessions:
        return True
    else:
        return False
