# COSMIC Desktop Theming & Frosted Glass Architecture

- **COSMIC Release Tested**: Epoch 1 (Arch Linux `cosmic-session` 1:1.11.0-1, `cosmic-comp` 1:1.11.0-1)
- **Configuration Directory**: `~/.config/cosmic/` (per-user) and `/usr/share/cosmic/` (system-wide defaults)
- **Data Serialization**: RON (Rusty Object Notation) and atomic plain values.

---

## 1. Setting to File Mapping

| Setting | UI Path in `cosmic-settings` | Config File / RON Path | Live-Apply | Scriptable | Verified Notes |
|---|---|---|---|---|---|
| **Frosted Glass (Global)** | Desktop > Appearance > Frosted Glass | `com.system76.CosmicTheme.Dark.Builder/v2/frosted` | Yes | Yes | Values: `ExtremelyLow`, `VeryLow`, `Low`, `Medium`, `High`, `VeryHigh`, `ExtremelyHigh` |
| **Frosted Windows** | Desktop > Appearance > Window Transparency | `com.system76.CosmicTheme.Dark.Builder/v2/frosted_windows` | Yes | Yes | Boolean: `true` / `false` |
| **Frosted Panel** | Desktop > Appearance > Panel Blur | `com.system76.CosmicTheme.Dark.Builder/v2/frosted_panel` | Yes | Yes | Boolean: `true` / `false` |
| **Frosted Applets** | Desktop > Appearance > Applets Blur | `com.system76.CosmicTheme.Dark.Builder/v2/frosted_applets` | Yes | Yes | Boolean: `true` / `false` |
| **Frosted System Interface** | Desktop > Appearance > System Surfaces | `com.system76.CosmicTheme.Dark.Builder/v2/frosted_system_interface` | Yes | Yes | Boolean: `true` / `false` |
| **Accent Color** | Desktop > Appearance > Color Palette > Accent | `com.system76.CosmicTheme.Dark.Builder/v2/accent` | Yes | Yes | Format: `Some((<R>, <G>, <B>))` or `None` (default Sydra Blue `#5B8DEF` is `(0.357, 0.553, 0.937)`) |
| **Background Color** | Desktop > Appearance > Background | `com.system76.CosmicTheme.Dark.Builder/v2/bg_color` | Yes | Yes | Tint base for dark theme (default Sydra Graphite `#12141A` is `(0.071, 0.078, 0.102)`) |
| **Corner Radii** | Desktop > Appearance > Corner Roundness | `com.system76.CosmicTheme.Dark.Builder/v2/corner_radii` | Yes | Yes | RON tuple for `radius_0` through `radius_xl` |
| **Window Gaps** | Desktop > Window Management > Gaps | `com.system76.CosmicTheme.Dark.Builder/v2/gaps` | Yes | Yes | Format: `(outer, inner)` e.g. `(0, 8)` |
| **Desktop Wallpaper** | Desktop > Wallpaper | `com.system76.CosmicBackground/v1/all` | Yes | Yes | RON struct with `source: Path("/path/to/image")` |
| **Top Panel Config** | Desktop > Panel & Dock > Top Panel | `com.system76.CosmicPanel.Panel/v1/` | Yes | Yes | Controls `anchor`, `opacity`, `size`, `plugins_wings`, `plugins_center` |
| **Bottom Dock Config** | Desktop > Panel & Dock > Dock | `com.system76.CosmicPanel.Dock/v1/` | Yes | Yes | Controls `anchor: Bottom`, `autohide`, `border_radius`, `opacity` |
| **Dark / Light Mode** | Desktop > Appearance > Style | `com.system76.CosmicTheme.Mode/v1/is_dark` | Yes | Yes | Boolean: `true` / `false` |
| **Terminal Font** | Terminal > Settings | `com.system76.CosmicTerm/v1/font_name` | Yes | Yes | String e.g. `"JetBrains Mono"` |
| **Terminal Opacity** | Terminal > Settings | `com.system76.CosmicTerm/v1/opacity` | Yes | Yes | Float e.g. `0.88` |

---

## 2. Non-COSMIC Application Theming

- **GTK 3 / GTK 4 Apps**: COSMIC writes GTK settings into `~/.config/gtk-3.0/` and `~/.config/gtk-4.0/` via `dconf` and `adw-gtk-theme`. GTK windows adhere to dark color scheme matching COSMIC.
- **Qt 6 Applications** (Sydra Game Hub, Welcome App, Calamares): Styled using `qt6ct` and `kvantum` engine. Kvantum renders dark glass translucent frames and buttons matching Sydra tokens.
- **Electron Apps** (VS Code): Opaque dark surface with matching `#12141A` title bar and accents.
