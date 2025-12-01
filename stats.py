
# stats.py
import pandas as pd
from espn_api.football import League

teamMap = {
    1: 'Barrett', 2: 'Clint', 3: 'Parker', 4: 'Miller', 5: 'Justin', 6: 'Jack',
    7: 'Kenny', 8: 'Chris', 9: 'Steven', 10: 'Waller', 11: 'Tucci', 12: 'Hutch'
}

LEAGUE_ID = 440494
import os
ESPN_S2 = os.getenv("ESPN_S2")
SWID = os.getenv("SWID")

def get_fantasy_stats(YEAR=2025, WEEK=None):
    league = League(
        league_id=LEAGUE_ID, year=YEAR,
        espn_s2=ESPN_S2, swid=SWID
    )

    if WEEK is None:
        WEEK = league.currentMatchupPeriod

    box_scores = league.box_scores(WEEK)

    # stat containers
    hero = {'player': '', 'projected': 0, 'actual': 0, 'gap': 0, 'team': ''}
    zero = {'player': '', 'projected': 0, 'actual': 0, 'gap': 999, 'team': ''}
    bench_mvp = {'player': '', 'points': 0, 'team': ''}
    mvp = {'player': '', 'points': 0, 'team': ''}
    closest_match = {'winner': '', 'loser': '', 'margin': float('inf')}
    biggest_blowout = {'winner': '', 'loser': '', 'margin': 0}
    best_by_position = {}

    # ---------- WEEKLY CALCULATIONS ----------
    for match in box_scores:
        for side in [
            {'team_obj': match.home_team, 'lineup': match.home_lineup},
            {'team_obj': match.away_team, 'lineup': match.away_lineup}
        ]:
            for p in side['lineup']:
                if p.points is None or p.projected_points is None:
                    continue

                delta = p.points - p.projected_points

                if delta > hero['gap'] and p.lineupSlot not in ['BE', 'IR']:
                    hero = {
                        'player': p.name,
                        'projected': p.projected_points,
                        'actual': p.points,
                        'gap': delta,
                        'team': side['team_obj'].team_id
                    }

                if delta < zero['gap'] and p.lineupSlot not in ['BE', 'IR']:
                    zero = {
                        'player': p.name,
                        'projected': p.projected_points,
                        'actual': p.points,
                        'gap': delta,
                        'team': side['team_obj'].team_id
                    }

                if p.lineupSlot in ['BE', 'IR'] and p.points > bench_mvp['points']:
                    bench_mvp = {
                        'player': p.name,
                        'points': p.points,
                        'team': side['team_obj'].team_id
                    }

                if p.points > mvp['points'] and p.lineupSlot not in ['BE', 'IR']:
                    mvp = {
                        'player': p.name,
                        'points': p.points,
                        'team': side['team_obj'].team_id
                    }

        margin = abs(match.home_score - match.away_score)
        if margin < closest_match['margin'] and margin > 0:
            winner = match.home_team.team_id if match.home_score > match.away_score else match.away_team.team_id
            loser = match.away_team.team_id if match.home_score > match.away_score else match.home_team.team_id
            closest_match = {'winner': winner, 'loser': loser, 'margin': margin}

        if margin > biggest_blowout['margin']:
            winner = match.home_team.team_id if match.home_score > match.away_score else match.away_team.team_id
            loser = match.away_team.team_id if match.home_score > match.away_score else match.home_team.team_id
            biggest_blowout = {'winner': winner, 'loser': loser, 'margin': margin}

    # ---------- BEST POSITION PLAYERS ----------
    for pos in ["QB", "RB", "WR", "TE", "K", "D/ST"]:
        for t in league.teams:
            for p in t.roster:
                if p.position == pos and p.posRank == 1:
                    best_by_position[pos] = {
                        'player': p.name,
                        'points': p.total_points,
                        'team': teamMap.get(p.onTeamId, "Unknown")
                    }

    # ---------- ALL-TIME POINTS ----------
    total_points_history = {team_id: 0 for team_id in teamMap.keys()}

    for y in range(2015, YEAR+1):
        try:
            ly = League(league_id=LEAGUE_ID, year=y, espn_s2=ESPN_S2, swid=SWID)
            for t in ly.standings():
                total_points_history[t.team_id] += t.points_for
        except:
            pass

    total_df = (
        pd.Series(total_points_history)
        .rename("total_points")
        .reset_index()
        .rename(columns={"index": "team_id"})
    )
    total_df["team"] = total_df["team_id"].map(teamMap)
    total_df = total_df.sort_values("total_points", ascending=False)

    # Return everything as JSON-serializable
    return {
        "week": WEEK,
        "hero": hero,
        "zero": zero,
        "mvp": mvp,
        "bench_mvp": bench_mvp,
        "closest": {
            **closest_match,
            "winner_name": teamMap.get(closest_match["winner"], ""),
            "loser_name": teamMap.get(closest_match["loser"], "")
        },
        "blowout": {
            **biggest_blowout,
            "winner_name": teamMap.get(biggest_blowout["winner"], ""),
            "loser_name": teamMap.get(biggest_blowout["loser"], "")
        },
        "best_by_position": best_by_position,
        "all_time_points": total_df.to_dict(orient="records")
    }