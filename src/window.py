# window.py
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

import gi, math

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from typing import Union, Any, Dict
from gi.repository import Adw, Gdk, Gio, GLib, Gtk
from .define import RES_PATH
from .pages import main_page
from .components import Shortcuts

resource = f"{RES_PATH}/window.ui"

def string_to_color(string: str):
  colors = {
    "light": Adw.ColorScheme.FORCE_LIGHT,
    "default": Adw.ColorScheme.DEFAULT,
    "dark": Adw.ColorScheme.FORCE_DARK,
  }
  return colors[string]

def create_main_window(application: Adw.Application):
  builder = Gtk.Builder.new_from_resource(resource)
  settings = application.utils.settings
  window = builder.get_object("window")
  content = builder.get_object("content")
  menu_button = builder.get_object("menu_button")
  info = builder.get_object("info")
  source = builder.get_object("source")

  def load_window_state():
    settings.bind(
      key="width",
      object=window,
      property="default-width",
      flags=Gio.SettingsBindFlags.DEFAULT,
    )
    settings.bind(
      key="height",
      object=window,
      property="default-height",
      flags=Gio.SettingsBindFlags.DEFAULT,
    )
    settings.bind(
      key="is-maximized",
      object=window,
      property="maximized",
      flags=Gio.SettingsBindFlags.DEFAULT,
    )
    settings.bind(
      key="is-fullscreen",
      object=window,
      property="fullscreened",
      flags=Gio.SettingsBindFlags.DEFAULT,
    )
    window.set_help_overlay(Shortcuts())

  def load_main_page():
    content.set_child(main_page(application))

  def open_uri(link: str):
    Gtk.show_uri(
      window,
      link,
      Gdk.CURRENT_TIME
    );

  load_window_state()
  load_main_page()
  window.set_application(application)
  window.set_icon_name(application.get_application_id())
  window.load_main_page = load_main_page
  return window
