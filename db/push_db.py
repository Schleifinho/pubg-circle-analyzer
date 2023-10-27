# region Imports
import peewee
from db.db import Tournaments, TelemetryLogGameStatePeriodicEventServer, TelemetryLogGameStatePeriodicLiveServer, \
    LiveServerMatchData, TournamentMatchData
from helper.my_logger import logger


# endregion

# region Push To DB
def push_tournament_list(tournament_list):
    mapped_tournament_list = [{"id": element["id"], "type": element["type"],
                               "createdAt": element["attributes"]["createdAt"]} for element in tournament_list]

    for tourney in mapped_tournament_list:
        try:
            Tournaments.create(**tourney)
        except Exception as e:
            logger.debug(e)


def push_telemetry_log_event_server(_id, _elapsedTime, _numAliveTeams, _numAlivePlayers, _poisonGasWarningPositionX,
                                    _poisonGasWarningPositionY, _poisonGasWarningRadius, _isGame, _matchId):
    try:
        TelemetryLogGameStatePeriodicEventServer.create(id=_id,
                                                        elapsedTime=_elapsedTime,
                                                        numAliveTeams=_numAliveTeams,
                                                        numAlivePlayers=_numAlivePlayers,
                                                        poisonGasWarningPositionX=_poisonGasWarningPositionX,
                                                        poisonGasWarningPositionY=_poisonGasWarningPositionY,
                                                        poisonGasWarningRadius=_poisonGasWarningRadius,
                                                        isGame=_isGame,
                                                        matchId=_matchId
                                                        )
    except peewee.PeeweeException as e:
        logger.debug(e)


def push_telemetry_log_live_server(_id, _elapsedTime, _numAliveTeams, _numAlivePlayers, _poisonGasWarningPositionX,
                                   _poisonGasWarningPositionY, _poisonGasWarningRadius, _isGame, _matchId):
    try:
        TelemetryLogGameStatePeriodicLiveServer.create(id=_id,
                                                       elapsedTime=_elapsedTime,
                                                       numAliveTeams=_numAliveTeams,
                                                       numAlivePlayers=_numAlivePlayers,
                                                       poisonGasWarningPositionX=_poisonGasWarningPositionX,
                                                       poisonGasWarningPositionY=_poisonGasWarningPositionY,
                                                       poisonGasWarningRadius=_poisonGasWarningRadius,
                                                       isGame=_isGame,
                                                       matchId=_matchId
                                                       )
    except peewee.PeeweeException as e:
        logger.debug(e)


def push_live_server_match_data(_matchId, _mapName, _isCustomMatch, _duration, _shardId, _gameMode, _createdAt,
                                _matchType, _telemetryURL):
    try:
        LiveServerMatchData.create(matchId=_matchId,
                                   mapName=_mapName,
                                   isCustomMatch=_isCustomMatch,
                                   duration=_duration,
                                   shardId=_shardId,
                                   gameMode=_gameMode,
                                   createdAt=_createdAt,
                                   matchType=_matchType,
                                   telemetryURL=_telemetryURL,
                                   )
    except peewee.PeeweeException as varname:
        logger.debug(varname)


def push_tournament_match_data(_matchId, _mapName, _isCustomMatch, _duration, _shardId, _gameMode, _createdAt,
                               _matchType, _telemetryURL, _tournamentId):
    try:
        TournamentMatchData.create(matchId=_matchId,
                                   mapName=_mapName,
                                   isCustomMatch=_isCustomMatch,
                                   duration=_duration,
                                   shardId=_shardId,
                                   gameMode=_gameMode,
                                   createdAt=_createdAt,
                                   matchType=_matchType,
                                   telemetryURL=_telemetryURL,
                                   tournamentId=_tournamentId
                                   )
    except peewee.PeeweeException as varname:
        logger.debug(varname)


def push_tournament(_id, _type, _createdAt):
    try:
        Tournaments.create(id=_id, type=_type, createdAt=_createdAt)
    except peewee.PeeweeException as e:
        logger.debug(e)
# endregion
