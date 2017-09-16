module.exports = {
    database: {
        client: 'sqlite3',
        connection: {
            filename: 'content/data/ghost-dev.db'
        }
    },
    migrationPath: process.cwd() + '/node_modules/ghost/core/server/data/migrations',
    currentVersion: '1.0.0'
}
