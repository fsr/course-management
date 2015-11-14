import functools
import collections

from django.shortcuts import render


def adaptive_render(func):

    @functools.wraps(func)
    def inner(request, *args, extra_context=None, **kwargs):
        extra_context = extra_context if extra_context is not None else {}

        def wrapped_render(*args_2, context=None, **kwargs_2):
            if context is None:
                if len(args_2) > 2:
                    a1, a2, context, *a = args_2
                    return render(a1, a2, collections.ChainMap(context, extra_context), *a, **kwargs_2)
                else:
                    context = {}
            return render(*args_2, context=extra_context.update(context), **kwargs)

        return func(request, *args, render=wrapped_render, **kwargs)

    return inner
