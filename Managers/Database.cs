﻿// Blu-Ray Discord Bot
//
// Copyright © 2020, The Blu-Ray authors 
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program. If not, see <http://www.gnu.org/licenses/>.

using DSharpPlus;
using Microsoft.Data.Sqlite;
using System;
using System.IO;
using System.Threading.Tasks;

namespace Bot.Managers
{
    public class Database
    {
        private static SqliteConnection sqlite;

        public static async Task ConnectAsync(string databasePath, DebugLogger logger)
        {
            bool prepare = !File.Exists(databasePath);
            sqlite = new SqliteConnection($"Data Source={databasePath}");

            sqlite.StateChange += (s, e) => logger.LogMessage(LogLevel.Info, "Database", $"State change: {e.OriginalState} -> {e.CurrentState}.", DateTime.Now);

            await sqlite.OpenAsync();
            if (prepare) await initializeAsync();
        }

        public static SqliteTransaction CreateTransaction() => sqlite.BeginTransaction();
        public static SqliteCommand CreateCommand()         => sqlite.CreateCommand();

        internal static async Task initializeAsync()
        {
            SqliteTransaction transaction   = CreateTransaction();
            SqliteCommand command           = CreateCommand();

            command.CommandText =   "create table starboardChannels ("                      +
                                    "   guildId     bigint(18)      not null unique,"       +
                                    "   channelId   bigint(18)      not null,"              +
                                    "   emoji       varchar(100)    not null,"              +
                                    "   amount      int             not null"               +
                                    ");"                                                    +
                                    " "                                                     +
                                    "create table starboardMessages ("                      +
                                    "   guildId             bigint(18) not null unique,"    +
                                    "   channelId           bigint(18) not null,"           +
                                    "   messageId           bigint(18) not null,"           +
                                    "   starboardMessageId  bigint(18) not null"            +
                                    ");"                                                    +
                                    " "                                                     +
                                    "create table tags ("                                   +
                                    "   guildId bigint(18)      not null unique,"           +
                                    "   userId  bigint(18)      not null,"                  +
                                    "   content varchar(2000)   not null"                   +
                                    ");";

            await command.ExecuteNonQueryAsync();
            transaction.Commit();
        }

        public static void Disconnect()
        {
            sqlite.Close();
            sqlite.Dispose();
        }
    }
}
