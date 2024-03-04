# region Imports
from peewee import fn
from db.db import TournamentMatchData, LiveServerMatchData, TelemetryLogGameStatePeriodicEventServer, \
    TelemetryLogGameStatePeriodicLiveServer, Tournaments


# endregion

# region Fetching


def fetch_event_server_matches(_map, date, due_date):
    return (TournamentMatchData.select().where(TournamentMatchData.mapName == _map)
                                        .where(date <= TournamentMatchData.createdAt <= due_date)
                                        .where(TournamentMatchData.createdAt <= date))


def fetch_live_server_matches(_map, date, due_date):
    return (LiveServerMatchData.select().where(LiveServerMatchData.mapName == _map)
                                        .where(date <= LiveServerMatchData.createdAt)
                                        .where(LiveServerMatchData.createdAt <= due_date))


def fetch_telemetry_data(server, matches_esport_live, zone, or_greater=False, or_less=False):
    matches_esport = matches_esport_live[0]
    matches_live = matches_esport_live[1]

    if server == "live":
        return fetch_live_server_telemetry(matches_live, zone, or_greater=or_greater, or_less=or_less)
    elif server == "esport":
        return fetch_event_server_telemetry(matches_esport, zone, or_greater=or_greater, or_less=or_less)
    else:
        telemetry = list(fetch_live_server_telemetry(matches_live, zone, or_greater=or_greater, or_less=or_less))
        telemetry += list(fetch_event_server_telemetry(matches_esport, zone, or_greater=or_greater, or_less=or_less))
        return telemetry


def fetch_event_server_telemetry_by_zones(matches, zone_list):
    return TelemetryLogGameStatePeriodicEventServer.select(
        TelemetryLogGameStatePeriodicEventServer.matchId,
        TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX,
        TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY,
        fn.GROUP_CONCAT(TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX).alias('poisonGasXGroup'),
        fn.GROUP_CONCAT(TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY).alias(
            'poisonGasYGroup')).where(
        TelemetryLogGameStatePeriodicEventServer.matchId.in_(matches)).where(
        TelemetryLogGameStatePeriodicEventServer.isGame.in_(zone_list)).order_by(
        TelemetryLogGameStatePeriodicEventServer.isGame).group_by(
        TelemetryLogGameStatePeriodicEventServer.matchId).execute()



def fetch_live_server_telemetry_by_zones(matches, zone_list):
    return TelemetryLogGameStatePeriodicLiveServer.select(
        TelemetryLogGameStatePeriodicLiveServer.matchId,
        TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX,
        TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY,
        fn.GROUP_CONCAT(TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX).alias('poisonGasXGroup'),
        fn.GROUP_CONCAT(TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY).alias(
            'poisonGasYGroup')).where(
        TelemetryLogGameStatePeriodicLiveServer.matchId.in_(matches)).where(
        TelemetryLogGameStatePeriodicLiveServer.isGame.in_(zone_list)).order_by(
        TelemetryLogGameStatePeriodicLiveServer.isGame).group_by(
        TelemetryLogGameStatePeriodicLiveServer.matchId)


def fetch_event_server_telemetry(matches, zone, or_greater, or_less):
    if or_greater and not or_less:
        return TelemetryLogGameStatePeriodicEventServer.select(
            TelemetryLogGameStatePeriodicEventServer.matchId,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY,
            fn.MAX(TelemetryLogGameStatePeriodicEventServer.isGame)).where(
            TelemetryLogGameStatePeriodicEventServer.matchId.in_(matches)).where(
            TelemetryLogGameStatePeriodicEventServer.isGame >= zone).group_by(
            TelemetryLogGameStatePeriodicEventServer.matchId)
    elif not or_greater and or_less:
        return TelemetryLogGameStatePeriodicEventServer.select(
            TelemetryLogGameStatePeriodicEventServer.matchId,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY,
            fn.MAX(TelemetryLogGameStatePeriodicEventServer.isGame)).where(
            TelemetryLogGameStatePeriodicEventServer.matchId.in_(matches)).where(
            TelemetryLogGameStatePeriodicEventServer.isGame <= zone).group_by(
            TelemetryLogGameStatePeriodicEventServer.matchId)
    elif not or_greater and not or_less:
        return TelemetryLogGameStatePeriodicEventServer.select(
            TelemetryLogGameStatePeriodicEventServer.matchId,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY,
            TelemetryLogGameStatePeriodicEventServer.isGame).where(
            TelemetryLogGameStatePeriodicEventServer.matchId.in_(matches)).where(
            TelemetryLogGameStatePeriodicEventServer.isGame == zone)
    else:
        return TelemetryLogGameStatePeriodicEventServer.select(
            TelemetryLogGameStatePeriodicEventServer.matchId,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicEventServer.poisonGasWarningPositionY,
            TelemetryLogGameStatePeriodicEventServer.isGame).where(
            TelemetryLogGameStatePeriodicEventServer.matchId.in_(matches))


def fetch_live_server_telemetry(matches, zone, or_greater, or_less):
    if or_greater and not or_less:
        return TelemetryLogGameStatePeriodicLiveServer.select(
            TelemetryLogGameStatePeriodicLiveServer.matchId,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY,
            fn.MAX(TelemetryLogGameStatePeriodicLiveServer.isGame)).where(
            TelemetryLogGameStatePeriodicLiveServer.matchId.in_(matches)).where(
            TelemetryLogGameStatePeriodicLiveServer.isGame >= zone).group_by(
            TelemetryLogGameStatePeriodicLiveServer.matchId)
    elif not or_greater and or_less:
        return TelemetryLogGameStatePeriodicLiveServer.select(
            TelemetryLogGameStatePeriodicLiveServer.matchId,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY,
            fn.MAX(TelemetryLogGameStatePeriodicLiveServer.isGame)).where(
            TelemetryLogGameStatePeriodicLiveServer.matchId.in_(matches)).where(
            TelemetryLogGameStatePeriodicLiveServer.isGame <= zone).group_by(
            TelemetryLogGameStatePeriodicLiveServer.matchId)
    elif not or_greater and not or_less:
        return TelemetryLogGameStatePeriodicLiveServer.select(
            TelemetryLogGameStatePeriodicLiveServer.matchId,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY,
            TelemetryLogGameStatePeriodicLiveServer.isGame).where(
            TelemetryLogGameStatePeriodicLiveServer.matchId.in_(matches)).where(
            TelemetryLogGameStatePeriodicLiveServer.isGame == zone)
    else:
        return TelemetryLogGameStatePeriodicLiveServer.select(
            TelemetryLogGameStatePeriodicLiveServer.matchId,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionX,
            TelemetryLogGameStatePeriodicLiveServer.poisonGasWarningPositionY,
            TelemetryLogGameStatePeriodicLiveServer.isGame).where(
            TelemetryLogGameStatePeriodicLiveServer.matchId.in_(matches))


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


def fetch_tournament_by_date_and_type(date, _type=None):
    if type:
        return Tournaments.select().where(Tournaments.createdAt > date).where(Tournaments.type == _type)
    else:
        return Tournaments.select().where(Tournaments.createdAt > date)


def fetch_tournament_id_by_date(date):
    return Tournaments.select(Tournaments.id).where(Tournaments.createdAt > date)


def fetch_tournaments_by_ids_list(tournament_ids):
    return Tournaments.select().where(Tournaments.id.in_(tournament_ids))


def fetch_matches(server, _map, date, due_date):
    if server == "live":
        return None, fetch_live_server_matches(_map, date, due_date)
    elif server == "esport":
        return fetch_event_server_matches(_map, date, due_date), None
    else:
        match_data_live = fetch_live_server_matches(_map, date, due_date)
        match_data_esport = fetch_event_server_matches(_map, date, due_date)
        return match_data_esport, match_data_live


def fetch_telemetry_data_poison_zone_per_phase(server, matches_esport_live, zones):
    matches_esport = matches_esport_live[0]
    matches_live = matches_esport_live[1]
    if server == "live":
        return fetch_live_server_telemetry_by_zones(matches_live, zones)
    elif server == "esport":
        return fetch_event_server_telemetry_by_zones(matches_esport, zones)
    else:
        results = list(fetch_live_server_telemetry_by_zones(matches_live, zones))
        results += list(fetch_event_server_telemetry_by_zones(matches_esport, zones))
        return results
# endregion
