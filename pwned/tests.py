import unittest, collections, random, datetime
import pwned.competitions, pwned.client, pwned.support

class PwnedTests(unittest.TestCase):
    def setUp(self):
        self.pwned_client = pwned.client.Pwned('http://api.pwned.localhost/', 'abc', '123')

    def test_create_tournament(self):
        settings = {
            'name': 'Python Client Test #' + str(random.randint(1, 400000000)),
            'game_id': 3,
            'players_on_team': 5,
            'country_id': 1,
            'template': 'singleelim16',
        }
        
        tournament = self.create_tournament(settings)
        
        self.assertIsInstance(tournament, pwned.competitions.Tournament)
        self.assertEqual(tournament.name, settings['name'])
        self.assertEqual(int(tournament.game.id), settings['game_id'])
        self.assertEqual(tournament.template, settings['template'])
        self.assertEqual(tournament.players_on_team, settings['players_on_team'])
        self.assertEqual(tournament.team_count, 16)
        self.assertEqual(tournament.round_count, 4)
        self.assertIsNotNone(tournament.client)
        
    def test_get_rounds(self):
        tournament = self.create_tournament({'template': 'singleelim8'})
        
        rounds = tournament.get_rounds()
        
        self.assertEqual(len(rounds), 3)
        self.assertEqual(len(rounds[0].stages), 1)
        self.assertEqual(len(rounds[0].stages[0].matches), 4)
        
        for round in rounds:
            self.assertTrue(round.round_number)
            self.assertTrue(round.identifier)
            self.assertTrue(round.stages)
            
            for stage in round.stages:
                self.assertTrue(stage.matches)
                
                for match in stage.matches:
                    self.assertTrue(match.id)

    def test_get_round(self):
        tournament = self.create_tournament({'template': 'singleelim8'})
        
        round = tournament.get_round(2)
        
        self.assertEqual(len(round.stages), 1)
        self.assertEqual(len(round.stages[0].matches), 2)
        
        for match in round.stages[0].matches:
            self.assertTrue(match.id)

    def test_update_round(self):
        league = self.create_league()
        
        rounds = league.get_rounds()
        
        rounds[0].name = 'This is my round. It is a nice round.'
        rounds[0].time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        league.update_round(rounds[0])
        
        fetched_rounds = league.get_rounds()
        
        self.assertEqual(rounds[0].name, fetched_rounds[0].name)
        self.assertEqual(rounds[0].time, fetched_rounds[0].time)
            
    def test_add_signup(self):
        settings = {
            'name': 'Python Signup Test #' + str(random.randint(1, 400000000)),
            'seeding': 2,
            'contact': 'Random Name #' + str(random.randint(1, 400000000)),
        }
        
        signup = self.create_signup(settings)
    
        tournament = self.create_tournament()
        tournament.add_signups([signup])
        
        fetched_tournament = self.pwned_client.get_tournament(tournament.id)
        signups = fetched_tournament.get_signups()
        
        self.assertEqual(int(fetched_tournament.signup_count), 1)
        self.assertEqual(len(signups), 1)
        self.assertEqual(signups[0].name, settings['name'])
        self.assertEqual(signups[0].contact, settings['contact'])
        self.assertEqual(int(signups[0].seeding), settings['seeding'])

    def test_remove_signup(self):
        settings = {
            'name': 'Python Signup Test #' + str(random.randint(1, 400000000)),
            'seeding': 2,
            'contact': 'Random Name #' + str(random.randint(1, 400000000)),
        }
        
        signup = self.create_signup(settings)
    
        tournament = self.create_tournament()
        tournament.add_signups([signup])
        
        fetched_tournament = self.pwned_client.get_tournament(tournament.id)
        signups = fetched_tournament.get_signups()
        
        self.assertEqual(int(fetched_tournament.signup_count), 1)
        self.assertEqual(len(signups), 1)
        
        tournament.remove_signup(signups[0])
        
        fetched_tournament = self.pwned_client.get_tournament(tournament.id)
        signups = fetched_tournament.get_signups()
        
        self.assertEqual(int(fetched_tournament.signup_count), 0)
        self.assertEqual(len(signups), 0)
    
    def test_set_match_result(self):
        tournament = self.create_tournament({'template': 'singleelim4'})
        
        matches = tournament.get_round(1).stages[0].matches
        
        self.assertEqual(len(matches), 2)
        called = False

        for match in matches:
            score = random.randint(1, 50)
            score_opponent = random.randint(1, 50)
            
            match.score = score
            match.score_opponent = score_opponent
            
            tournament.update_match(match)
            
            match_fetched = tournament.get_match(match.id)
            
            self.assertEqual(str(match.score), str(match_fetched.score))
            self.assertEqual(str(match.score_opponent), str(match_fetched.score_opponent))
            
            called = True
            
        self.assertTrue(called)
    
    def test_create_league(self):
        settings = {
            'name': 'Python Client Test #' + str(random.randint(1, 400000000)),
            'league_type': 'league',
            'team_count': 4,
            'game_id': 3,
            'players_on_team': 5,
            'country_id': 1,
            'scoring_model_id': 1,
        }
        
        league = self.create_league(settings)
        
        self.assertIsInstance(league, pwned.competitions.League)
        self.assertEqual(league.name, settings['name'])
        self.assertEqual(int(league.game.id), settings['game_id'])
        self.assertEqual(league.players_on_team, settings['players_on_team'])
        self.assertEqual(int(league.team_count), 4)
        self.assertEqual(league.league_type, 'league')
        self.assertIsNotNone(league.client)

        self.assertEqual(int(league.scoring_model.id), settings['scoring_model_id'])
        self.assertEqual(int(league.scoring_model.points_win), 3)
    
    def test_league_league_score_calculation(self):
        settings = {
            'name': 'Python Client Test #' + str(random.randint(1, 400000000)),
            'league_type': 'league',
            'team_count': 4,
            'game_id': 3,
            'players_on_team': 5,
            'country_id': 1,
            'scoring_model_id': 1,
        }
        
        league = self.create_league(settings)    
        self.assertIsInstance(league, pwned.competitions.League)
        
        league.add_signups(self.create_signups(4))
        league.start()
        matches = league.get_round(1).stages[0].matches
        
        matches[0].score = 6
        matches[0].score_opponent = 9
        
        matches[1].score = 15
        matches[1].score_opponent = 0
        
        league.update_match(matches[0])
        league.update_match(matches[1])
        
        table = league.get_table()
        
        self.assertEqual(len(table), 4)
        
        self.assertEqual(table[0].signup.id, matches[1].signup.id)
        self.assertEqual(table[1].signup.id, matches[0].signup_opponent.id)
        self.assertEqual(table[2].signup.id, matches[0].signup.id)
        self.assertEqual(table[3].signup.id, matches[1].signup_opponent.id)
        
        self.assertEqual(1, table[0].position)
        self.assertEqual(1, table[0].wins)
        self.assertEqual(0, table[0].draws)
        self.assertEqual(0, table[0].losses)
        self.assertEqual(3, table[0].points)
        self.assertEqual(15, table[0].score)
        self.assertEqual(15, table[0].score_for)
        self.assertEqual(0, table[0].score_against)
        
        self.assertEqual(2, table[1].position)
        self.assertEqual(3, table[2].position)
        self.assertEqual(4, table[3].position)
        
        self.assertEqual(1, table[2].losses)
        
        self.assertEqual(3, table[1].score)
        self.assertEqual(9, table[1].score_for)
        self.assertEqual(6, table[1].score_against)
        
        self.assertEqual(-3, table[2].score)
        self.assertEqual(-15, table[3].score)
    
    def test_league_championship_score_calculation(self):
        settings = {
            'name': 'Python Client Test #' + str(random.randint(1, 400000000)),
            'league_type': 'championship',
            'round_count': 4,
            'team_count': 8,
            'game_id': 3,
            'country_id': 1,
            'scoring_model_id': 2,
        }
        
        league = self.create_league(settings)    
        self.assertIsInstance(league, pwned.competitions.League)
        self.assertEqual(4, league.round_count)
        self.assertEqual(4, len(league.get_rounds()))
        
        league.add_signups(self.create_signups(8))
        league.start()
        
        signups = league.get_signups()
        
        random.shuffle(signups)
        results = []
        i = 1
        
        for signup in signups:
            results.append(pwned.support.LeagueChampionshipRoundResultEntry(signup=signup, position=i, score=1000 - i*50))
            i += 1
            
        league.set_championship_round_results(1, results)
        
        table = league.get_table()
        self.assertEqual(8, len(table))
        expected_scores = (25, 18, 15, 12, 10, 8, 6, 4)
        i = 0
        
        for signup in signups:
            self.assertEqual(signup.id, table[i].signup.id)
            self.assertEqual(i+1, table[i].position)
            self.assertEqual(1000 - (i+1)*50, table[i].score)
            self.assertEqual(expected_scores[i], table[i].points)
            
            i += 1
            
        self.assertEqual(i, 8)
        
        league_fetched = self.pwned_client.get_league(league.id)
        self.assertEqual(league.id, league_fetched.id)
        self.assertEqual(2, league_fetched.round_current)
    
    def test_get_league_scoring_models(self):
        scoring_models = self.pwned_client.get_league_scoring_models()
        
        self.assertNotEqual(0, len(scoring_models))
        
        for scoring_model in scoring_models:
            self.assertTrue(scoring_model.id)
            self.assertTrue(scoring_model.name)
            self.assertTrue(scoring_model.type)
            
            if scoring_model.type == 'championship':
                self.assertNotEqual(0, len(scoring_model.points_position))
            else:
                self.assertTrue(scoring_model.points_win)
    
    def test_get_league_scoring_models_by_type(self):
        self.assertNotEqual(0, len(self.pwned_client.get_league_scoring_models('championship')))
        self.assertNotEqual(0, len(self.pwned_client.get_league_scoring_models('league')))
        
    def test_get_league_scoring_model(self):
        scoring_model = self.pwned_client.get_league_scoring_model(1)
        
        self.assertEqual(1, scoring_model.id)
        self.assertTrue(scoring_model.name)
        self.assertTrue(scoring_model.type)
    
    def test_create_scoring_model(self):
        values = {
            'type': 'league',
            'name': 'Create Scoring Model ' + str(random.randint(1, 4000000)),
            'description': 'This is a description ' + str(random.randint(1, 4000000)),
            'points_win': 3,
            'points_draw': 2,
            'points_loss': 1,
        }
    
        scoring_model = pwned.support.LeagueScoringModel(**values)
        scoring_model_created = self.pwned_client.create_league_scoring_model(scoring_model)
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        
        self.assertEqual(scoring_model_fetched.type, values['type'])
        self.assertEqual(scoring_model_fetched.name, values['name'])
        self.assertEqual(scoring_model_fetched.description, values['description'])
        self.assertEqual(scoring_model_fetched.points_win, values['points_win'])
        self.assertEqual(scoring_model_fetched.points_draw, values['points_draw'])
        self.assertEqual(scoring_model_fetched.points_loss, values['points_loss'])
        
        self.pwned_client.delete_league_scoring_model(scoring_model_fetched.id)
    
    def test_update_scoring_model(self):
        values = {
            'type': 'league',
            'name': 'Create Scoring Model ' + str(random.randint(1, 4000000)),
            'description': 'This is a description ' + str(random.randint(1, 4000000)),
            'points_win': 3,
            'points_draw': 2,
            'points_loss': 1,
        }
    
        scoring_model = pwned.support.LeagueScoringModel(**values)
        scoring_model_created = self.pwned_client.create_league_scoring_model(scoring_model)
        scoring_model_created.name = 'Updated Scoring Model' + str(random.randint(1, 4000000))
        scoring_model_created.description = 'Updated description ' + str(random.randint(1, 4000000))
        
        self.pwned_client.update_league_scoring_model(scoring_model_created)
        
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        
        self.assertEqual(scoring_model_fetched.name, scoring_model_created.name)
        self.assertEqual(scoring_model_fetched.description, scoring_model_created.description)
    
    def test_delete_scoring_model(self):
        values = {
            'type': 'league',
            'name': 'Create Scoring Model ' + str(random.randint(1, 4000000)),
            'description': 'This is a description ' + str(random.randint(1, 4000000)),
            'points_win': 3,
            'points_draw': 2,
            'points_loss': 1,
        }
    
        scoring_model = pwned.support.LeagueScoringModel(**values)
        scoring_model_created = self.pwned_client.create_league_scoring_model(scoring_model)
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        self.assertTrue(scoring_model_fetched.id)
        
        self.pwned_client.delete_league_scoring_model(scoring_model_fetched.id)
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        
        self.assertFalse(scoring_model_fetched.active)

    def test_restore_scoring_model(self):
        values = {
            'type': 'league',
            'name': 'Create Scoring Model ' + str(random.randint(1, 4000000)),
            'description': 'This is a description ' + str(random.randint(1, 4000000)),
            'points_win': 3,
            'points_draw': 2,
            'points_loss': 1,
        }
    
        scoring_model = pwned.support.LeagueScoringModel(**values)
        scoring_model_created = self.pwned_client.create_league_scoring_model(scoring_model)
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        self.assertTrue(scoring_model_fetched.id)
        
        self.pwned_client.delete_league_scoring_model(scoring_model_fetched.id)
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        
        self.assertFalse(scoring_model_fetched.active)
        
        scoring_model_fetched.active = True
        self.pwned_client.update_league_scoring_model(scoring_model_fetched)
        scoring_model_fetched = self.pwned_client.get_league_scoring_model(scoring_model_created.id)
        self.assertTrue(scoring_model_fetched.active)
    
    def test_get_games(self):
        games = self.pwned_client.get_games()
        
        self.assertNotEqual(len(games), 0)
        
        for game in games:
            self.assertTrue(game.name)
            self.assertTrue(game.id)
    
    def test_get_tournament_templates(self):
        templates = self.pwned_client.get_tournament_templates()
    
        self.assertNotEqual(len(templates), 0)
        
        for template in templates:
            self.assertTrue(template.template)
            self.assertTrue(template.teams)

    def test_get_countries(self):
        countries = self.pwned_client.get_countries()
        
        self.assertNotEqual(len(countries), 0)
        
        for country in countries:
            self.assertTrue(country.id)
            self.assertTrue(country.code)
            self.assertTrue(country.language_key)
            self.assertTrue(country.country_key)
            
    def create_tournament(self, settings = None):
        settings_default = {
            'name': 'Python Client Test Tournament',
            'game_id': 3,
            'players_on_team': 5, 
            'country_id': 1, 
            'template': 'singleelim8',
        }
        
        if isinstance(settings, collections.Mapping):
            settings_default.update(settings)
        
        tournament = pwned.competitions.Tournament(**settings_default)
        
        return self.pwned_client.create_tournament(tournament)
    
    def create_signup(self, settings=None):
        settings_default = {
            'name': 'Python Signup Test #' + str(random.randint(1, 400000000)),
            'has_server': True,
            'contact': 'Random Signup Name #' + str(random.randint(1, 400000000)),
            'remoteId': str(random.randint(1, 400000000)),
        }
        
        if isinstance(settings, collections.Mapping):
            settings_default.update(settings)
            
        return pwned.support.Signup(**settings_default)
    
    def create_signups(self, count, settings=None):
        signups = []
        
        for i in range(0, count):
            signups.append(self.create_signup(settings))
            
        return signups
    
    def create_league(self, settings = None):
        settings_default = {
            'name': 'Python Client Test League',
            'league_type': 'league',
            'game_id': 3,
            'players_on_team': 5, 
            'country_id': 1, 
            'team_count': 8,
            'scoring_model_id': 1,
        }
        
        if isinstance(settings, collections.Mapping):
            settings_default.update(settings)
        
        league = pwned.competitions.League(**settings_default)
        
        return self.pwned_client.create_league(league)