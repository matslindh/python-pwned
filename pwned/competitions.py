from pwned.support import Game, LeagueScoringModel

class Competition:
    _fields = {
        'id': 'id',
        'name': 'name',
        'gameId': 'game_id',
        'playersOnTeam': 'players_on_team',
        'countryId': 'country_id',
        'language': 'language',
        'description': 'description',
        'lastActivityAt': 'last_activity_at',
        'liveAt': 'live_at',
        'teamCount': 'team_count',
        'roundCount': 'round_count',
        'roundCurrent': 'round_current',
        'demandGUIDs': 'demand_guids',
        'onlyRegistered': 'only_registered',
        'signupMode': 'signup_mode',
        'signupCount': 'signup_count',
        'path': 'path',
    }
    
    def __init__(self, **args):
        for f in self._fields:
            k = self._fields[f]
            
            if k in args:
                setattr(self, k, args[k])
                
        self.game = None
        self.client = None
        
        if 'game' in args:
            self.game = args['game']
            
        if 'client' in args:
            self.client = args['client']
    
    def get_api_dict(self, *args):
        fields = self._fields
        
        for el in args:
            fields = dict(list(fields.items()) + list(el.items()))
        
        response = {}
        
        for f in fields:
            if hasattr(self, fields[f]):
                response[f] = getattr(self, fields[f])
        
        return response
    
    @classmethod
    def from_api_call(cls, specific_class, data, fields=None, client=None):
        if fields is None:
            fields = {}
            
        fields = dict(list(fields.items()) + list(cls._fields.items()))
        arguments = {}

        for f in fields:
            if f in data:
                arguments[fields[f]] = data[f]
                
        if 'game' in data:
            arguments['game'] = Game.from_api_call(data['game'])
        
        if client:
            arguments['client'] = client
            
        return specific_class(**arguments)

    def create(self, client):
        return getattr(client, 'create_' + self._get_type())(self)

    def start(self, client=None):
        client = self._get_client(client)
        client.start(self._get_type(), self.id)
        
    def add_signups(self, signups, client=None):
        client = self._get_client(client)
        return client.add_signups(self._get_type(), self.id, signups)
    
    def get_signups(self, client=None):
        client = self._get_client(client)
        
        return client.get_signups(self._get_type(), self.id)
        
    def remove_signup(self, signup, client=None):
        client = self._get_client(client)
        return client.remove_signup(self._get_type(), self.id, signup.id)

    def get_round(self, round_index, client=None):
        client = self._get_client(client)
        
        return client.get_round(self._get_type(), self.id, round_index)
        
    def update_round(self, round, client=None):
        client = self._get_client(client)
        
        return client.update_round(self._get_type(), self.id, round)
        
    def get_rounds(self, client=None):
        client = self._get_client(client)
        
        return client.get_rounds(self._get_type(), self.id)
    
    def get_match(self, match_id, client=None):
        client = self._get_client(client)
        
        return client.get_match(self._get_type(), self.id, match_id)

    def update_match(self, match, client=None):
        client = self._get_client(client)
        
        return client.update_match(self._get_type(), self.id, match)
    
    def _get_type(self):
        return self.__class__.__name__.lower()
    
    def _get_client(self, client=None):
        if not client:
            return self.client
        
        return client
        
class Tournament(Competition):
    __fields = {
        'template': 'template',
        'groupSize': 'group_size',
        'groupCount': 'group_count',
        'quickProgress': 'quick_progress',
    }
    
    def __init__(self, **args):
        super().__init__(**args)

        for f in self.__fields:
            k = self.__fields[f]
            
            if k in args:
                setattr(self, k, args[k])        

    def get_api_dict(self):
        return super().get_api_dict(self.__fields)
        
    @classmethod
    def from_api_call(cls, data, client=None):
        return Competition.from_api_call(cls, data, cls.__fields, client=client)
    
class League(Competition):
    __fields = {
        'leagueType': 'league_type',
        'teamCount': 'team_count',
        'scoringModelId': 'scoring_model_id',
        'roundCount': 'round_count',
    }

    def __init__(self, **args):
        super().__init__(**args)

        for f in self.__fields:
            k = self.__fields[f]
            
            if k in args:
                setattr(self, k, args[k])
    
        self.scoring_model = None
        
        if 'scoring_model' in args:
            self.scoring_model = args['scoring_model']
    
    def get_api_dict(self):
        return super().get_api_dict(self.__fields)
    
    @classmethod
    def from_api_call(cls, data, client=None):
        league = Competition.from_api_call(cls, data, cls.__fields, client=client)
        
        if 'scoringModel' in data:
            league.scoring_model = LeagueScoringModel.from_api_call(data['scoringModel'])
        
        return league
        
    def get_table(self, client=None):
        client = self._get_client(client)
        
        return client.get_league_table(self.id)
        
    def set_championship_round_results(self, round_number, results, client=None):
        client = self._get_client(client)
        
        return client.league_set_championship_round_results(self.id, round_number, results)
