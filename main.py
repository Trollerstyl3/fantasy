import datetime

from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yf
import datetime as dt

oauth = OAuth2(None, None, from_file='oauth2.json')

# Positions:
# PG
# SG
# SF
# PF
# Util
# BN
# IL


# get game
gm = yf.Game(oauth, 'nba')

# Check leagues
# for i in gm.league_ids(2021):
#     f = gm.to_league(i).settings()
#     print(f['name'], f['league_key'])

# id for bassmen bois 410.l.72284
_lg = gm.to_league('410.l.72284')

# get access to user team get teamkey
_tm = _lg.to_team(_lg.team_key())


def setActive(lg, tm, date):
    # get roster and get players and eligible positions
    roster = tm.roster()
    players = {}
    for i in roster:
        id = i['player_id']
        elig = i['eligible_positions']
        players[id] = elig

    # Check what to player
    avail = rosterSpots(lg)

    changes = []

    for p in players:
        if 'IL' in players[p]:
            if check_avail(avail, 'IL'):
                avail['IL'] -= 1
                changes.append({'player_id': p, 'selected_position': 'IL'})
        else:
            pass


def check_played(pl, date) -> bool:
    pass


def check_avail(avail, status) -> bool:
    if avail[status] > 0:
        return True
    return False


def rosterSpots(lg):
    out = {}
    pos = lg.position()
    for i in pos:
        out[i] = int(pos[i]['count'])
    return out


print(_tm.roster())
