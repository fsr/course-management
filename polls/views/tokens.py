import string

from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, render_to_response

from polls.models import Poll, Token

from polls.util.permissions import must_be_owner

allowed_chars = string.ascii_letters + string.digits


@permission_required('token.create')
def generate(request, poll_name):
    amount = request.GET.get('amount', None)
    poll = Poll.objects.get(url=poll_name)
    context = {
        'poll': poll,
        'generate': True
    }

    if amount is not None:
        tokens = [
            Token.generate(poll)
            for _ in range(amount)
        ]
        context['tokens'] = tokens
    return render(
        request,
        'polls/gen.html',
        context
    )


# URL does not exist atm
@login_required
def generate_user_token(request, poll_name):
    poll = Poll.objects.get(url=poll_name)
    try:
        t = Token.objects.get(
            poll=poll,
            user=request.user
        )
        return render_to_response(
            'polls/error/has_token.html',
            { 'token': t }
        )
    except Token.DoesNotExist:
        token = Token.generate(
            poll=poll,
                user=request.user
        )
        return render(
            request,
            'polls/tokens.html',
            {'tokens': [token]}
        )


@login_required
@must_be_owner
def all(request, poll_name):
    poll = Poll.objects.get(url=poll_name)
    return render(
        request,
        'polls/tokens.html',
        {'tokens': poll.tokens}
    )
