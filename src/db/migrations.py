# migrations.py
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

from .seed import seed_from_json
from ..define import RES_PATH

SCHEMA_VERSION = 1

def run_migrations(db):
  db.execute("""
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER NOT NULL
    )
  """)

  cur = db.execute("SELECT version FROM schema_version")
  row = cur.fetchone()

  if row is None:
    db.execute("INSERT INTO schema_version (version) VALUES (?)", (SCHEMA_VERSION,))
    create_v1(db)
  elif row["version"] < SCHEMA_VERSION:
    upgrade(db, row["version"])

def create_v1(db):
  create_brand_table(db)
  create_vehicle_type_table(db)
  create_fuel_type_table(db)
  create_fuel_table(db)
  create_vehicle_model_table(db)
  create_vehicle_table(db)

  seed_from_json(db, table_name="fuel_type")
  seed_from_json(db, table_name="fuel")
  seed_from_json(db, table_name="vehicle_type")
  seed_from_json(db, table_name="brand")

def upgrade(db, from_version: int):
  if from_version < 1:
    create_v1(db)

  db.execute(
      "UPDATE schema_version SET version = ?",
      (SCHEMA_VERSION,)
  )


## Fuels
def create_fuel_type_table(db):
  db.execute(
    """
    CREATE TABLE IF NOT EXISTS fuel_type (
      id          TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
      name        TEXT NOT NULL,
      description TEXT
    );
    """
  )
  db.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_fuel_type_name ON fuel_type(name);
    """
  )

def create_fuel_table(db):
  db.execute(
    """
    CREATE TABLE IF NOT EXISTS fuel (
      id            TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
      name          TEXT NOT NULL,
      fuel_type_id  TEXT NOT NULL,
      description   TEXT,

      FOREIGN KEY (fuel_type_id) REFERENCES fuel_type(id)
    );
    """
  )
  db.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_fuel_unique ON fuel(name, fuel_type_id);
    """
  )

## Brand
def create_brand_table(db):
  db.execute(
    """
    CREATE TABLE IF NOT EXISTS brand (
      id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
      name            TEXT,
      country_code    TEXT NOT NULL,
      year_foundation INTEGER,
      founders        TEXT,
      website         TEXT
    );
    """
  )
  db.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_brand_name ON brand(name);
    """
  )


## Vehicle
def create_vehicle_type_table(db):
  db.execute(
    """
    CREATE TABLE IF NOT EXISTS vehicle_type (
        id               TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
        name             TEXT NOT NULL,
        description      TEXT,
        category         TEXT,
        typical_use      TEXT,
        average_size     TEXT,
        common_features  TEXT,
        classification   TEXT,
        created_at       TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """
  )


def create_vehicle_model_table(db):
  db.execute(
    """
    CREATE TABLE IF NOT EXISTS vehicle_model (
      id              TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
      brand_id        TEXT NOT NULL,
      name            TEXT NOT NULL,
      vehicle_type_id TEXT NOT NULL,

      FOREIGN KEY (brand_id) REFERENCES brand(id),
      FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_type(id)
    );
    """
  )
  db.execute(
    """
    CREATE UNIQUE INDEX IF NOT EXISTS idx_vehicle_model_unique ON vehicle_model (brand_id, name);
    """
  )

def create_vehicle_table(db):
  db.execute(
    """
    CREATE TABLE IF NOT EXISTS vehicle (
      id               TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
      name             TEXT NOT NULL,
      type_id          TEXT NOT NULL,
      brand_id         TEXT NOT NULL,
      model_id         TEXT NOT NULL,
      plate            TEXT NOT NULL UNIQUE,
      vehicle_year     INTEGER NOT NULL,
      measurement_unit TEXT NOT NULL CHECK (
        measurement_unit IN ('kilometers', 'miles')
      ),
      chassis          TEXT,
      notes            TEXT,
      color            TEXT,
      active           INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1)),
      created_at       TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at       TEXT,

      FOREIGN KEY (brand_id) REFERENCES brand(id),
      FOREIGN KEY (model_id) REFERENCES vehicle_model(id),
      FOREIGN KEY (type_id) REFERENCES vehicle_type(id)
    );
    """
  )

  # utils index
  db.execute("CREATE INDEX IF NOT EXISTS idx_vehicle_name ON vehicle(name)")
