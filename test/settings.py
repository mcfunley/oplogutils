# We run two copies, one started with the --master flag and one
# without it.  Tools that alter the oplog need the master to be
# started with no replication options.
MONGOD_PORT = 27027
MONGOD_REPLICATION_PORT = 27028

MONGOD_TEMP_PORT = 27029

FIXTURES_COPY = 'fixtures.2'
FIXTURES_TEMP = 'fixtures.3'


