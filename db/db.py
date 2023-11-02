# region Imports
from peewee import Model, MySQLDatabase, CharField, BooleanField, IntegerField, ForeignKeyField, \
    DateTimeField, FloatField

from config.db_config import DATABASE, HOST, PASSWORD, USER

# endregion

# region Create DB
mysqlDB = MySQLDatabase(database=DATABASE, user=USER, password=PASSWORD, host=HOST)


# endregion

# region Live Data
class LiveServerMatchData(Model):
    matchId = CharField(primary_key=True)
    mapName = CharField()
    isCustomMatch = BooleanField()
    duration = IntegerField()
    shardId = CharField()
    gameMode = CharField()
    createdAt = DateTimeField()
    matchType = CharField()
    telemetryURL = CharField()

    class Meta:
        database = mysqlDB


class TelemetryLogGameStatePeriodicLiveServer(Model):
    id = CharField(primary_key=True)
    elapsedTime = IntegerField()
    numAliveTeams = IntegerField()
    numAlivePlayers = IntegerField()
    poisonGasWarningPositionX = FloatField()
    poisonGasWarningPositionY = FloatField()
    poisonGasWarningRadius = FloatField()
    isGame = FloatField()
    matchId = ForeignKeyField(LiveServerMatchData, backref='TelemetryLogGameStatePeriodicLiveServer',
                              column_name="matchId")

    class Meta:
        database = mysqlDB


# endregion

# region Tournament Data
class Tournaments(Model):
    id = CharField(primary_key=True)
    type = CharField()
    createdAt = DateTimeField()

    class Meta:
        database = mysqlDB


class TournamentMatchData(Model):
    matchId = CharField(primary_key=True)
    mapName = CharField()
    isCustomMatch = BooleanField()
    duration = IntegerField()
    shardId = CharField()
    gameMode = CharField()
    createdAt = DateTimeField()
    matchType = CharField()
    telemetryURL = CharField()
    tournamentId = ForeignKeyField(Tournaments, backref='tournamentMatchData', column_name="tournamentId")

    class Meta:
        database = mysqlDB


class TelemetryLogGameStatePeriodicEventServer(Model):
    id = CharField(primary_key=True)
    elapsedTime = IntegerField()
    numAliveTeams = IntegerField()
    numAlivePlayers = IntegerField()
    poisonGasWarningPositionX = FloatField()
    poisonGasWarningPositionY = FloatField()
    poisonGasWarningRadius = FloatField()
    isGame = FloatField()
    matchId = ForeignKeyField(TournamentMatchData, backref='TelemetryLogGameStatePeriodicEventServer',
                              column_name="matchId")

    class Meta:
        database = mysqlDB

# endregion
