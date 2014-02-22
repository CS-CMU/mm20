from config.handle_constants import retrieveConstants
# from unittest import TestCase, main
from action import Action

actionBuffer = {}
actionDispatch = {}


def response(status_code, **kwargs):
    kwargs["status"] = status_code
    return kwargs

_TODO = response(500, message="not yet implemented")
_INVALID = response(404, message="invalid call")


def gatherActions(action, *args, **kwargs):
    action = Action(action, args, kwargs)
    actionBuffer[action.key] = action


def handleAction(action):
    """action handler"""
    if action in actionDispatch:
        return actionDispatch[action.key](action.args, action.kwargs)
    else:
        return response(404, message="invalid call")


def _movePlayer(*args, **kwargs):
    if room in kwargs and player in kwargs:
        return kwargs[player].move(k[room])
    else:
        return _INVALID
    # return _TODO
actionDispatch['movePlayer'] = _movePlayer


def _eatFood(*args, **kwargs):
    if foodTable in kwargs and player in kwargs:
        return kwargs[player].eat(kwargs[foodTable])
    else:
        return _INVALID
    # return _TODO
actionDispatch['eatFood'] = _eatFood


def _sleep(*args, **kwargs):
    if player in kwargs and arguments in kwargs:
        return kwargs[player].sleep(k[arguments]) 
        # implement sleep function in team_member
        # arguments are whatever args in sleep function
    else:
        return _INVALID

    # return _TODO
actionDispatch['sleep'] = _sleep


def _code(*args, **kwargs):
    if player in kwargs and arguments in kwargs:
        return kwargs[player].code(k[arguments])
        # implement code function
        # arguments are whatever args in code function
    else:
        return _INVALID
    # return _TODO
actionDispatch['code'] = _code


def _getMap(*args, **kwargs):
    return _TODO
actionDispatch['getMap'] = _getMap


def _info(*args, **kwargs):
    return _TODO
actionDispatch['info'] = _info


def _serverInfo(*args, **kwargs):
    constants = retrieveConstants('generalInfo')
    return response(200, version=constants.VERSION, name=constants.NAME)
actionDispatch['serverInfo'] = _serverInfo
