python-pwned
============

A python client library for accessing the API of pwned.no

See pwned/tests.py for extensive usage examples.

Creating a league
-----------------

    settings = {
        'name': 'Python Client Test League',
        'league_type': 'league',
        'game_id': 3,
        'players_on_team': 5, 
        'country_id': 1, 
        'team_count': 8,
        'scoring_model_id': 1,
    }
    
    league = pwned.competitions.League(**settings)
    league_created = pwned_client.create_league(league)
    
    # .. or you can create the League object directly (which **settings will expand to)
    league = pwned.competitions.League(name="My League", league_type="League", team_count=8, scoring_model_id=1)
    
Retrieving list of defined games
--------------------------------

    games = self.pwned_client.get_games()
    
Get rounds
----------

    rounds = league.get_rounds()
    
Get specific round
------------------

    round = league.get_round(1)
    
Get matches in a round
----------------------

    round = league.get_round(1)
    
    # each round will have at least one stage (or possibly in double elimination or other variants, several)
    matches = round.stages[0].matches
    
Get current league table standings
----------------------------------

    table = league.get_table()
    