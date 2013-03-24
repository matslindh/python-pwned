import collections

class Game:
    _fields = {
        'id': ('id', ),
        'name': ('name', ),
        'teamBased': ('team_based', ),
        'privateServers': ('private_servers', ),
        'active': ('active', ),
        'defaultLeagueType': ('default_league_type', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)
        
class LeagueScoringModel:
    _fields = {
        'id': ('id', ),
        'type': ('type', ),
        'name': ('name', ),
        'description': ('description', ),
        'active': ('active', ),
        'winPoints': ('points_win', ),
        'drawPoints': ('points_draw', ),
        'lossPoints': ('points_loss', ),
        'positionPoints': ('points_position', ),
        'bonusPoints': ('points_bonus', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)        
        
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class Signup:
    _fields = {
        'id': ('id', ),
        'name': ('name', ),
        'hasServer': ('has_server', ),
        'isAccepted': ('is_accepted', ),
        'onWaitingList': ('on_waiting_list', ),
        'contact': ('contact', ),
        'seeding': ('seeding', ),
        'clanId': ('clan_id', ),
        'remoteId': ('remote_id', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class Match:
    _fields = {
        'id': ('id', ),
        'signup': ('signup', Signup),
        'signupOpponent': ('signup_opponent', Signup),
        'score': ('score', ),
        'scoreOpponent': ('score_opponent', ),
        'seeding': ('seeding', ),
        'seedingOpponent': ('seeding_opponent', ),
        'isWalkover': ('is_walkover', ),
        'time': ('time', ),
        'mapName': ('map_name', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class Group:
    _fields = {
    
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)
        
class RoundStage:
    _fields = {
        'mapName': ('map_name', ),
        'description': ('description', ),
        'time': ('time', ),
        'matches': ('matches', Match),
    }
    
    def __init__(self, *args, **kwargs):
        self.matches = []
        
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class Round:
    _fields = {
        'roundNumber': ('round_number', ),
        'identifier': ('identifier', ),
        'name': ('name', ),
        'description': ('description', ),
        'time': ('time', ),
        'startedAt': ('started_at', ),
        'stages': ('stages', RoundStage),
        'groups': ('groups', Group),
    }
    
    def __init__(self, *args, **kwargs):
        self.stages = []
        self.groups = []
        
        object_init_impl(self, *args, **kwargs)
        
    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class LeagueTablePosition:
    _fields = {
        'signup': ('signup', Signup),
        'position': ('position', ),
        'wins': ('wins', ),
        'draws': ('draws', ),
        'losses': ('losses', ),
        'points': ('points', ),
        'score': ('score', ),
        'scoreFor': ('score_for', ),
        'scoreAgainst': ('score_against', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class LeagueChampionshipRoundResultEntry:
    _fields = {
        'signup': ('signup', Signup),
        'position': ('position', ),
        'score': ('score', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)

class TournamentTemplate:
    _fields = {
        'description': ('description', ),
        'template': ('template', ),
        'teams': ('teams', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)        

class Country:
    _fields = {
        'id': ('id', ),
        'code': ('code', ),
        'languageKey': ('language_key', ),
        'countryKey': ('country_key', ),
        'defaultLanguage': ('default_language', ),
    }
    
    def __init__(self, *args, **kwargs):
        object_init_impl(self, *args, **kwargs)

    def get_api_dict(self, *args, **kwargs):
        return get_api_dict_impl(self, *args, **kwargs)
                
    @classmethod
    def from_api_call(*args, **kwargs):
        return from_api_call_impl(*args, **kwargs)        
        
def get_api_dict_impl(obj, *args):
    fields = obj._fields
    
    for el in args:
        fields = dict(list(fields.items()) + list(el.items()))
    
    response = {}
    
    for f in fields:
        if hasattr(obj, fields[f][0]):
            response[f] = getattr(obj, fields[f][0])
            
            if response[f] and (len(fields[f]) > 1):
                if isinstance(response[f], collections.Sequence):
                    val = []
                    
                    for el in response[f]:
                        val.append(el.get_api_dict(*args))
                        
                    response[f] = val
                else:
                    response[f] = response[f].get_api_dict(*args)
    
    return response
        
def from_api_call_impl(cls, data):
    arguments = {}

    for f in cls._fields:
        if f in data:
            k = cls._fields
            
            if data[f] and (len(k[f]) > 1):
                # we can't check for iterables, as that would include dicts -- we only want actual lists
                if isinstance(data[f], (list, tuple)):
                    arguments[k[f][0]] = []
                    
                    for el in data[f]:
                        arguments[k[f][0]].append(k[f][1].from_api_call(el))
                else:
                    arguments[k[f][0]] = k[f][1].from_api_call(data[f])
            else:
                arguments[k[f][0]] = data[f]
    
    return cls(**arguments)

def object_init_impl(obj, *args, **kwargs):
    if 'client' in kwargs:
        obj.client = kwargs['client']

    for f in obj._fields:
        k = obj._fields[f][0]
        
        if k in kwargs:
            setattr(obj, k, kwargs[k])