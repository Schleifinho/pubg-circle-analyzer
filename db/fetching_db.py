from peewee import fn

from db.db import TournamentMatchData, LiveServerMatchData, TelemetryLogGameStatePeriodicEventServer, \
    TelemetryLogGameStatePeriodicLiveServer, Tournaments


def fetch_matches(server, _map, date):
    if server == "live":
        return None, fetch_live_server_matches(_map, date)
    elif server == "esport":
        return fetch_event_server_matches(_map, date), None
    else:
        match_data_live = fetch_live_server_matches(_map, date)
        match_data_esport = fetch_event_server_matches(_map, date)
        return match_data_esport, match_data_live


def fetch_event_server_matches(_map, date):
    return TournamentMatchData.select().where(TournamentMatchData.mapName == _map) \
        .where(TournamentMatchData.createdAt > date)


def fetch_live_server_matches(_map, date):
    return LiveServerMatchData.select().where(LiveServerMatchData.mapName == _map) \
        .where(LiveServerMatchData.createdAt > date)


def fetch_event_server_telemetry(matches):
    return TelemetryLogGameStatePeriodicEventServer.select(
        TelemetryLogGameStatePeriodicEventServer.matchId,
        TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX,
        TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY,
        fn.MAX(TelemetryLogGameStatePeriodicEventServer.isGame)).where(
        TelemetryLogGameStatePeriodicEventServer.matchId.in_(matches)).where(
        TelemetryLogGameStatePeriodicEventServer.isGame >= 7).group_by(TelemetryLogGameStatePeriodicEventServer.matchId)


def fetch_live_server_telemetry(matches):
    return TelemetryLogGameStatePeriodicLiveServer.select(
        TelemetryLogGameStatePeriodicLiveServer.matchId,
        TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX,
        TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY,
        fn.MAX(TelemetryLogGameStatePeriodicLiveServer.isGame)).where(
        TelemetryLogGameStatePeriodicLiveServer.matchId.in_(matches)).where(
        TelemetryLogGameStatePeriodicLiveServer.isGame >= 7).group_by(TelemetryLogGameStatePeriodicLiveServer.matchId)


def fetch_get_or_none_live_server_match_data(match_id):
    return LiveServerMatchData.get_or_none(LiveServerMatchData.matchId == match_id)


def fetch_get_or_none_telemetry_log_live_server(match_id):
    return TelemetryLogGameStatePeriodicLiveServer.get_or_none(
        TelemetryLogGameStatePeriodicLiveServer.matchId == match_id)


def fetch_get_or_none_tournament_match_data(match_id):
    return TournamentMatchData.get_or_none(TournamentMatchData.matchId == match_id)


def fetch_get_or_none_telemetry_log_tournament(match_id):
    return TelemetryLogGameStatePeriodicEventServer.get_or_none(
        TelemetryLogGameStatePeriodicEventServer.matchId == match_id)


def fetch_tournament_matches_by_tournament_id(tournament_id):
    return TournamentMatchData.select(TournamentMatchData.matchId).where(
        TournamentMatchData.tournamentId == tournament_id)


def fetch_tournament_by_date(date):
    return Tournaments.select().where(Tournaments.createdAt > date).where(Tournaments.type == "tournament")

