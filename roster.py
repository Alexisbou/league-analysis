from mwrogue.esports_client import EsportsClient

import datetime as dt
import requests


def fetch_games_from(date):
    site = EsportsClient("lol")

    response = site.cargo_client.query(
        tables="ScoreboardGames=SG, Tournaments=T",
        join_on="SG.OverviewPage=T.OverviewPage",
        fields="T.Name, SG.DateTime_UTC, SG.Team1, SG.Team2",
        where=f"SG.DateTime_UTC >= '{date}'",
    )

    return response


def fetch_results_between(start_dt, end_dt):
    site = EsportsClient("lol")
    response = site.cargo_client.query(
        tables="ScoreboardGames=SG, ScoreboardPlayers=SP, Tournaments=T",
        join_on="SG.GameId=SP.GameId, SG.OverviewPage=T.OverviewPage",
        fields="SG.GameId, T.Name=Tournament, SG.DateTime_UTC, SG.Team1, SG.Team2, SG.Winner, SG.Patch, SP.Link, SP.Team, SP.Champion, SP.SummonerSpells, SP.KeystoneRune, SP.Role, SP.GameId, SP.Side",
        where="SG.DateTime_UTC >= '" + str(start_dt) + " 00:00:00' AND SG.DateTime_UTC <= '" + str(
            end_dt) + " 00:00:00'"
    )

    return response


def fetch_score_board():
    site = EsportsClient("lol")
    result = site.cargo_client.query(
        tables='MatchScheduleGame=MSG,AcsMetadata=ACS',
        join_on='MSG.GameId=ACS.GameId',
        fields='MSG.MatchHistory=MatchHistory, MSG.GameId=GameId, MSG.OverviewPage=OverviewPage, MSG.MatchId=MatchId, MSG.N_GameInMatch=N_GameInMatch, MSG._pageName=Page',
        limit=10)

    return result


def test_fetch():
    # Create an instance of the EsportsClient
    client = EsportsClient('lol')

    # Define the Cargo table name
    cargo_table = "MatchScheduleGame"

    # Define the Cargo fields to fetch
    cargo_fields = ["Team1Bans", "Team2Bans"]

    # Define the query conditions (e.g., tournament name)
    query_conditions = {"Tournament": "LEC/2022 Season/Spring Season"}

    # Execute the Cargo query
    result = client.cargo_client.query(
        tables=cargo_table,
        fields=cargo_fields,
        # where=query_conditions,
        limit=10  # Adjust the limit as needed
    )

    # Check if the query was successful
    if result:
        # Extract picks and bans data from the result
        for row in result:
            team1_bans = row["Team1Bans"].split(",") if row.get("Team1Bans") else []
            team2_bans = row["Team2Bans"].split(",") if row.get("Team2Bans") else []

            print("Team 1 bans:", team1_bans)
            print("Team 2 bans:", team2_bans)
            print()
    else:
        print("Failed to fetch data")


def fetch_picks_and_bans(start_dt,end_dt):
    from mwclient import Site

    site = Site('lol.fandom.com', path='/')
    fields = [
        "MSG.GameId",
        "MSG.Blue",
        "MSG.Red",
        "MSG.Winner",
        *["PAB.Team{}Pick{}".format(i, j) for i in range(1, 3) for j in range(1, 6)],
        *["PAB.Team{}Ban{}".format(i, j) for i in range(1, 3) for j in range(1, 6)],
    ]

    # fields = ['Team1PicksByRoleOrder ','Team2PicksByRoleOrder ']

    response = site.api("cargoquery",
                        limit="max",
                        tables='MatchSchedule=MS,MatchScheduleGame=MSG,PicksAndBansS7=PAB',
                        fields=",".join(fields),
                        where="MS.DateTime_UTC >= '" + str(start_dt) + " 00:00:00' AND MS.DateTime_UTC <= '" + str(
                            end_dt) + " 00:00:00' AND MSG.Winner IS NOT NULL AND MS.Winner IS NOT NULL",
                        join_on="MS.MatchId=MSG.MatchId,MSG.GameId=PAB.GameID")

    return response['cargoquery']