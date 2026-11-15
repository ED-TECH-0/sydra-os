// 1. Setup Wallpaper on all screens
var desktopsArray = desktopsForActivity(currentActivity());
for (var j = 0; j < desktopsArray.length; j++) {
    desktopsArray[j].wallpaperPlugin = 'org.kde.image';
    desktopsArray[j].currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    desktopsArray[j].writeConfig("Image", "file:///usr/share/wallpapers/Sydra/contents/images/3840x2160.png");
}

// 2. Top Translucent Status Bar
var topBar = new Panel();
topBar.location = "top";
topBar.height = 2 * Math.floor(gridUnit * 1.8 / 2);
topBar.floating = true;

var kickoff = topBar.addWidget("org.kde.plasma.kickoff");
kickoff.currentConfigGroup = ["Shortcuts"];
kickoff.writeConfig("global", "Alt+F1");

topBar.addWidget("org.kde.plasma.marginsseparator");
topBar.addWidget("org.kde.plasma.systemtray");
topBar.addWidget("org.kde.plasma.digitalclock");

// 3. Left Floating Capsule Dock
var dock = new Panel();
dock.location = "left";
dock.height = 2 * Math.floor(gridUnit * 2.8 / 2);
dock.floating = true;
dock.alignment = "center";

var taskBar = dock.addWidget("org.kde.plasma.icontasks");
taskBar.currentConfigGroup = ["General"];
taskBar.writeConfig("launchers", [
    "applications:org.kde.dolphin.desktop",
    "applications:org.kde.konsole.desktop",
    "preferred://browser",
    "applications:siddha-gamehub.desktop",
    "applications:systemsettings.desktop"
]);

dock.addWidget("org.kde.plasma.marginsseparator");
dock.addWidget("org.kde.plasma.showdesktop");
