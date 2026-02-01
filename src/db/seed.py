# seed.py
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

import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio
import json

def resolve_refs(db, row):
  resolved = {}
  for key, value in row.items():
    if isinstance(value, str) and value.startswith("__REF__:"):
      _, table, name = value.split(":", 2)
      cur = db.execute(
        f"SELECT id FROM {table} WHERE name = ?",
        (name,)
      )
      ref = cur.fetchone()
      if ref is None:
        raise ValueError(f"Reference not found: {table}.{name}")
      resolved[key] = ref["id"]
    else:
      resolved[key] = value
  return resolved


def load_table_seed(table_name):
  data = Gio.resources_lookup_data(
      f'/io/github/idevecore/Motus/data/seeds/{table_name}.json',
      Gio.ResourceLookupFlags.NONE
  )

  json_text = data.get_data().decode("utf-8")
  return json.loads(json_text)

def seed_from_json(db, table_name, unique_field="name"):
  data = load_table_seed(table_name)

  for item in data:
    item = resolve_refs(db, item)
    columns = ", ".join(item.keys())
    placeholders = ", ".join("?" for _ in item)
    values = tuple(item.values())

    sql = f"""
    INSERT INTO {table_name} ({columns})
         SELECT {placeholders}
WHERE NOT EXISTS (
         SELECT 1
           FROM {table_name}
          WHERE {unique_field} = ?
    )
    """
    db.execute(sql, values + (item[unique_field],))

