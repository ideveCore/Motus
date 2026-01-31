<img heigth="128" src="data/icons/hicolor/scalable/apps/io.github.idevecore.Motus.svg" align="left" />

# Motus

Manage vehicles, costs, and maintenance of your fleet with ease.

## Building

###  Requirements
- Python 3 `python` 
- PyGObject `python-gobject` 
- GTK4 `gtk4` 
- libadwaita (>= 1.2.0) `libadwaita`
- Meson `meson` 
- Ninja `ninja` 
- D-Bus `python-dbus`

### Building from Git
```bash 
 git clone --recurse-submodules https://github.com/idevecore/motus.git
 cd motus
 meson builddir --prefix=/usr/local 
 sudo ninja -C builddir install
 ```

## Donate
If you like this project and have some spare money left, consider donating:

### Github Sponsors
<a href='https://github.com/sponsors/ideveCore'><img width='60' alt='Download on Flathub' src='https://github.githubassets.com/images/email/sponsors/mona.png'/></a>

## License 
 [GNU General Public License 3 or later](https://www.gnu.org/licenses/gpl-3.0.en.html)
