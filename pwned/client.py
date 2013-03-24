import urllib.request, urllib.parse, http.client
import json
import hmac, hashlib
import sys

import pwned.competitions

class Pwned:
    __version = '0'

    def __init__(self, base_url, public_key, private_key):
        if not base_url.endswith('/'):
            base_url = base_url + '/'
    
        self.base_url = base_url
        self.public_key = public_key
        self.private_key = private_key
        
    def create_tournament(self, tournament):
        response = self._request('tournaments', 'POST', tournament.get_api_dict())
        
        if response:
            return pwned.competitions.Tournament.from_api_call(response, client=self)
    
    def create_league(self, league):
        response = self._request('leagues', 'POST', league.get_api_dict())
        
        if response:
            return pwned.competitions.League.from_api_call(response, client=self)

    def get(self, type, id):
        if hasattr(self, 'get_' + str(type)):
            return getattr(self, 'get_' + str(type))(id)

        raise PwnedAPIException('Unknown type for get: ' + str(type))
    
    def get_league(self, id):
        response = self._get_competition('league', id)
        
        if response:
            return pwned.competitions.League.from_api_call(response, client=self)
    
    def get_tournament(self, id):
        response = self._get_competition('tournament', id)
        
        if response:
            return pwned.competitions.Tournament.from_api_call(response, client=self)

    def get_tournament_templates(self):
        response = self._request('tournaments/templates')
        
        if not response is None:
            templates = []
            
            for template in response:
                templates.append(pwned.support.TournamentTemplate.from_api_call(template))
        
            return templates
            
    def update(self, type, id, competition):
        return self._request(type + 's/' + str(id), 'POST', competition.get_api_dict())

    def start(self, type, id):
        return self._request(type + 's/' + str(id), 'POST', {'status': 'live'})
    
    def add_signups(self, type, competition_id, signups):
        data = []
        
        for signup in signups:
            data.append(signup.get_api_dict())
    
        return self._request(type + 's/' + str(competition_id) + '/signups', 'POST', data)
    
    def get_signups(self, type, competition_id):
        response = self._request(type + 's/' + str(competition_id) + '/signups')
        
        if not response is None:
            signups = []
            
            for el in response:
                signups.append(pwned.support.Signup.from_api_call(el))
        
            return signups
            
    def remove_signup(self, type, competition_id, signup_id):
        return self._request(type + 's/' + str(competition_id) + '/signups/' + str(signup_id), 'DELETE')

    def get_round(self, type, competition_id, round_index):
        response = self._request(type + 's/' + str(competition_id) + '/rounds/' + str(round_index))
        
        if not response is None:
            return pwned.support.Round.from_api_call(response)

    def get_rounds(self, type, competition_id):
        response = self._request(type + 's/' + str(competition_id) + '/rounds')
        
        if not response is None:
            rounds = []
            
            for el in response:
                rounds.append(pwned.support.Round.from_api_call(el))
        
            return rounds

    def get_match(self, type, competition_id, match_id):
        response = self._request(type + 's/' + str(competition_id) + '/matches/' + str(match_id))
        
        if not response is None:
            return pwned.support.Match.from_api_call(response)
            
    def update_match(self, type, competition_id, match):
        return self._request(type + 's/' + str(competition_id) + '/matches/' + str(match.id), 'POST', match.get_api_dict())
        
    def update_round(self, type, competition_id, round):
        return self._request(type + 's/' + str(competition_id) + '/rounds/' + round.round_number, 'POST', round.get_api_dict())

    def get_league_table(self, league_id):
        response = self._request('leagues/' + str(league_id) + '/table')
        
        if not response is None:
            table = []
            
            for position in response:
                table.append(pwned.support.LeagueTablePosition.from_api_call(position))
    
            return table

    def get_league_scoring_models(self, type=None):
        if type:
            response = self._request('leagues/scoringmodels/' + type)
        else:
            response = self._request('leagues/scoringmodels', 'GET')
        
        if not response is None:
            scoring_models = []
            
            for scoring_model in response:
                scoring_models.append(pwned.support.LeagueScoringModel.from_api_call(scoring_model))
            
            return scoring_models
            
    def league_set_championship_round_results(self, league_id, round_number, results):
        data = []
        
        for result in results:
            val = result.get_api_dict()
            val['signupId'] = val['signup']['id']
            data.append(val)
            
        return self._request('leagues/' + str(league_id) + '/rounds/' + str(round_number) + '/results', 'POST', data)

    def get_games(self):
        response = self._request('games')
        
        if not response is None:
            games = []
            
            for game in response:
                games.append(pwned.support.Game.from_api_call(game))
            
            return games
    
    def get_countries(self):
        response = self._request('countries')
        
        if not response is None:
            countries = []
            
            for country in response:
                countries.append(pwned.support.Country.from_api_call(country))
                
            return countries
    
    def _get_competition(self, type, id):
        return self._request(type + 's/' + str(id))
    
    def _request(self, resource, request_method = 'GET', data = None):
        if data:
            data = json.dumps(data)
        else:
            data = ''
        
        url = self.base_url + resource + self._url_query_string(resource, request_method, data)
        headers = {'Content-Type': 'application/json', 'User-Agent': self._user_agent(), }
        response = None

        try:
            if data:
                data = bytes(data.encode("utf-8"))
            else:
                data = None
            
            if request_method in ('GET', 'POST'):
                request = urllib.request.Request(url, data=data, headers=headers)
                response = urllib.request.urlopen(request).read()
            else:
                url_info = urllib.parse.urlparse(url)
                path = url_info.path
                
                if url_info.query:
                    path = path + '?' + url_info.query
                
                connection = http.client.HTTPConnection(url_info.netloc)
                connection.request(request_method, path, body=data, headers=headers)
                
                response = connection.getresponse().read()
                connection.close()
        except urllib.error.HTTPError as e:
            response = e.read()
        
        try:
            response = json.loads(response.decode("utf-8"))
        except ValueError:
            print(response)
            raise PwnedAPIException('Invalid JSON returned from server.', response)
        
        if ('error' in response) and response['error']:
            raise PwnedAPIException(response['error']['reason'])
        
        if 'result' in response:
            return response['result']
        
        return response
    
    def _url_query_string(self, resource, request_method, data):
        return '?' + urllib.parse.urlencode({
            'publicKey': self.public_key,
            'signature': self._signature(resource, request_method, data)
        })
    
    def _signature(self, resource, request_method, data):
        return hmac.new(self.private_key.encode('ascii'), bytes((self.public_key + '|' + request_method + '|' + resource + '|' + data).encode("utf-8")), hashlib.sha256).hexdigest()
        
    def _user_agent(self):
        return 'python-pwned-api/' + self.__version + '/' + '.'.join(str(x) for x in sys.version_info[0:3])
        
class PwnedAPIException(Exception):
    def __init__(self, message, raw_response = None):
        Exception.__init__(self, message)
        
        if raw_response:
            self.raw_response = raw_response
        else:
            self.raw_response = None
            
    def __repr__(self):
        if self.raw_response:
            return self.message + "\n\n" + raw_response
            
        return self.message