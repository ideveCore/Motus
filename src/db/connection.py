# connection.py
#
# Copyright 2026 Ideve Core
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sqlite3
from pathlib import Path
from gi.repository import GLib

class Database:
  _instance = None

  def __init__(self):
    data_dir = Path(GLib.get_user_data_dir()) / "motus"
    data_dir.mkdir(parents=True, exist_ok=True)

    self.db_path = data_dir / "motus.db"
    self.conn = sqlite3.connect(self.db_path)
    self.conn.row_factory = sqlite3.Row

    self._enable_foreign_keys()

  def _enable_foreign_keys(self):
    self.conn.execute("PRAGMA foreign_keys = ON;")

  @classmethod
  def get(cls):
    if cls._instance is None:
      cls._instance = Database()
    return cls._instance

  def execute(self, query, params=()):
    cur = self.conn.cursor()
    cur.execute(query, params)
    self.conn.commit()
    return cur

  def close(self):
    self.conn.close()

