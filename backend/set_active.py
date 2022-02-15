import datetime
from yahoo_oauth import OAuth2
import yahoo_fantasy_api as yf
import datetime as dt
import json

oauth = OAuth2(None, None, from_file='auth/oauth2.json')

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

# get current week and loop through the week to start each date
curr_week = _lg.current_week()
start, end = _lg.week_date_range(curr_week)
delta = datetime.timedelta(days=1)
if start <= datetime.date.today():
    start = datetime.date.today() + delta


# print(datetime.date.today() + delta)


def set_active(lg, tm, date):
    # get roster and get players and eligible positions
    roster = tm.roster()
    players = {}
    for i in roster:
        id = i['player_id']
        elig = i['eligible_positions']
        players[id] = elig

    # Check what to player
    avail = roster_spots(lg)

    changes = []

    for p in players:
        if 'IL' in players[p]:
            if check_avail(avail, 'IL'):
                avail['IL'] -= 1
                changes.append({'player_id': p, 'selected_position': 'IL'})
        else:
            if check_played(lg, p, date):
                for i in players[p]:
                    if check_avail(avail, i):
                        avail[i] -= 1
                        changes.append({'player_id': p, 'selected_position': i})
                        break
            else:
                changes.append({'player_id': p, 'selected_position': "BN"})

    return changes


def check_played(lg, pl, date) -> bool:
    with open("../data/schedule.json", "r") as f:
        schedule = json.load(f)
        if date.isoformat() in schedule:
            return lg.player_details(pl)[0]["editorial_team_abbr"].upper() in \
                   schedule[date.isoformat()]
        return False


def check_avail(avail, status) -> bool:
    if avail[status] > 0:
        return True
    return False


def roster_spots(lg):
    out = {}
    pos = lg.positions()
    for i in pos:
        out[i] = int(pos[i]['count'])
    return out


while start <= end:
    _tm.change_positions(start, set_active(_lg, _tm, start))
    start += delta
# print(_tm.roster())
