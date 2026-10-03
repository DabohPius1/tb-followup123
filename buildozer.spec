[app]
title = TB Follow-up Calculator
package.name = tbfollowup
package.domain = org.tbfollowup
source.dir = .
source.include_exts = py,json,png,jpg,kv
source.exclude_dirs = bin,.buildozer,.github,.git
version = 1.0
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.api = 33
android.minapi = 23
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True
