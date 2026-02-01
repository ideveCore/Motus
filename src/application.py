# application.py
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
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gio, GLib, Gtk
from .utils import Utils
from .window import create_main_window
from .actions import application_actions
from .db import Database, run_migrations

from .define import APP_ID, VERSION, RES_PATH

class Application(Adw.Application):
  """The main application singleton class."""

  def __init__(self):
    Adw.Application.__init__(
      self,
      application_id=APP_ID,
      resource_base_path=RES_PATH,
      flags=Gio.ApplicationFlags.DEFAULT_FLAGS
    )

    self.utils = Utils(APP_ID)
    application_actions(application=self)

  def do_startup(self):
    Adw.Application.do_startup(self)

    # Inicializa banco e garante schema
    db = Database.get()
    run_migrations(db)

  def do_activate(self):
    if self.get_active_window() is not None:
      self.get_active_window().present()
    else:
      create_main_window(self).present()
