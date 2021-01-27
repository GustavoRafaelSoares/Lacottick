CREATE TABLE IF NOT EXISTS guilds(
  GuildID integer PRIMARY KEY,
  Prefix text DEFAULT "l."
);

CREATE TABLE IF NOT EXISTS exp(
  UserID integer PRIMARY KEY,
  XP integer DEFAULT 0,
  level integer DEFAULT 0,
  XPLock text DEFAULT CURRENT_TIMESTAMP
);
