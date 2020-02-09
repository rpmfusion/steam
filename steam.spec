# Binary package, no debuginfo should be generated
%global debug_package %{nil}

Name:           steam
Version:        1.0.0.61
Release:        9%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file
License:        Steam License Agreement
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        http://repo.steampowered.com/%{name}/pool/%{name}/s/%{name}/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source4:        %{name}.appdata.xml
Source5:        README.Fedora

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist

# Input devices seen as joysticks:
Source6:        https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/after_kernel_4_9/51-these-are-not-joysticks-rm.rules

# Configure limits in systemd < 240
Source7:        01-steam.conf

# Updated UDEV rules
# https://github.com/ValveSoftware/steam-devices/commit/00aa8483cd243cbea9cff17fc113501aadc390b4
Patch0:         %{name}-udev-rules-update.patch

BuildRequires:  desktop-file-utils
BuildRequires:  systemd

# Required to run the initial setup
Requires:       tar
Requires:       zenity

# Most games use OpenGL, some games already use Vulkan. Vulkan is also required
# for Steam Play to run Windows games through emulation. i686 version of these
# packages are necessary even on x86_64 systems for running 32bit games. Pull in
# native arch drivers as well, by not specifying _isa macro, native arch
# packages are preferred. This will make sure people have all necessary drivers
# for both i686 and x86_64 games.
Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-dri-drivers
%if 0%{?fedora} || 0%{?rhel} > 7
# vulkan-drivers is only provided as x86_64 on EL7
# So CentOS altarch i386 will have none
# Just drop vulkan dependency there for now
Requires:       mesa-vulkan-drivers%{?_isa}
Requires:       mesa-vulkan-drivers
Requires:       vulkan-loader%{?_isa}
Requires:       vulkan-loader
%endif

# Minimum requirements for starting the steam client for the first time
Requires:       alsa-lib%{?_isa}
Requires:       gtk2%{?_isa}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       libnsl%{?_isa}
%endif
Requires:       libpng12%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXinerama%{?_isa}
Requires:       libXtst%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       mesa-libGL%{?_isa}
Requires:       nss%{?_isa}
Requires:       pulseaudio-libs%{?_isa}

# Required for sending out crash reports to Valve
Requires:       libcurl%{?_isa}

# Workaround for mesa-libGL dependency bug:
# https://bugzilla.redhat.com/show_bug.cgi?id=1168475
Requires:       systemd-libs%{?_isa}

# Required for the firewall rules
# http://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem

# Required for hardware decoding during In-Home Streaming (intel)
# Since libva-intel-driver on f28+ there is hw detection with appstream
%if 0%{?rhel} == 7
Requires:       libva-intel-driver%{?_isa}
%else
Requires:       libva%{?_isa}
%endif

# Required for hardware decoding during In-Home Streaming (radeon/nouveau)
Requires:       libvdpau%{?_isa}

# Required for having a functioning menu on the tray icon
Requires:       libdbusmenu-gtk3%{?_isa} >= 16.04.0

# Required by Feral interactive games
Requires:       libatomic%{?_isa}

# Required by Shank
Requires:       alsa-plugins-pulseaudio%{?_isa}

# Game performance is increased with gamemode (for games that support it)
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       gamemode
Requires:       gamemode%{?_isa}
# Recommends:     gnome-shell-extension-gamemode
%endif

Provides:       steam-noruntime = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      steam-noruntime < %{?epoch:%{epoch}:}%{version}-%{release}

%description
Installer for the Steam software distribution service.
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

%prep
%autosetup -p1 -n %{name}

sed -i 's/\r$//' %{name}.desktop
sed -i 's/\r$//' steam_subscriber_agreement.txt

cp %{SOURCE5} .

%build
# Nothing to build

%install
%make_install

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

mkdir -p %{buildroot}%{_udevrulesdir}/
install -m 644 -p lib/udev/rules.d/* \
    %{SOURCE6} %{buildroot}%{_udevrulesdir}/

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

# Environment files
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

# Install AppData
mkdir -p %{buildroot}%{_metainfodir}
install -p -m 0644 %{SOURCE4} %{buildroot}%{_metainfodir}/

# Since systemd 240 we don't need to raise NOFILE limit
%if 0%{?rhel} >= 7
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
%endif

%post
%if 0%{?rhel} == 7
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%endif

%files
%license COPYING steam_subscriber_agreement.txt
%doc README debian/changelog README.Fedora
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_metainfodir}/%{name}.appdata.xml
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_udevrulesdir}/*

# Since systemd 240 we don't need to raise NOFILE limit
%if 0%{?rhel} >= 7
%{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf
%endif

%changelog
* Sun Feb 09 2020 Simone Caronni <negativo17@gmail.com> - 1.0.0.61-9
- Update README.Fedora
- Require gamemode on Fedora & CentOS/RHEL 8.
- Adjust distribution conditionals.
- Make sure you are not left with the desktop when streaming with no option
  to get back to the Steam client.
- Update udev rules.

* Sat Nov 02 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.61-5
- Do not remove bundled libstdc++ (#5421).

* Sat Sep 07 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.61-4
- Firewall rules are now included in base firewalld also on RHEL/CentOS 7.

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.0.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 31 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.61-2
- Remove libdbusmenu-gtk2 requirement (#5322).

* Mon May 06 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.61-1
- Update to 1.0.0.61.

* Fri Mar 22 2019 Kamil Páral <kamil.paral@gmail.com> - 1.0.0.59-9
- add Recommends: gamemode

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.0.59-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jan 26 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.59-7
- Clean up SPEC file a bit.
- Update udev controller rules for Nvidia Shield Controller devices.

* Fri Jan 18 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.59-6
- Update udev controller rules to use uacces.

* Fri Jan 18 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.59-5
- Firewall definitions already bundled in firewalld 0.6.2 on Fedora 29+.
- Update firewall definitions to align with Fedora 29+.

* Wed Jan 16 2019 Simone Caronni <negativo17@gmail.com> - 1.0.0.59-4
- Fix Nvidia Shield Portable streaming with SteamLink.

* Wed Jan 02 2019 Kamil Páral <kamil.paral@gmail.com> - 1.0.0.59-3
- NOFILE limit doesn't need to be raised since F30 (systemd 240)
- fix macro condition check for vulkan libs

* Thu Dec 20 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0.59-2
- Drop vulkan on el7 for now

* Fri Dec 14 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.59-1
- Update to 1.0.0.59.

* Sun Dec 09 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.56-5
- Glibc in RHEL/CentOS 7 still provides libnsl.

* Sat Dec 01 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.56-4
- Add libnsl dependency (#5091).

* Fri Nov 02 2018 Kamil Páral <kamil.paral@gmail.com> - 1.0.0.56-3
- add systemd configuration for increasing file descriptor limit (for esync)

* Mon Oct 15 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.56-2
- Update Vulkan requirements for CentOS/RHEL 7.
- Update ports list for 11th October 2018 client.

* Thu Oct 11 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.56-1
- Update to 1.0.0.56.

* Wed Oct 10 2018 Kamil Páral <kamil.paral@gmail.com> - 1.0.0.54-20
- require vulkan drivers
- require x86_64 graphics drivers when installed on x86_64 systems

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.0.54-19
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Tue Jul 24 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-18
- Add firewalld-filesystem to BuildRequires to expand firewalld_reload macro.

* Tue Mar 27 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-17
- Re-add icon cache scriptlets for EPEL, as it's still required.
- Remove firewalld differences for EPEL.

* Tue Mar 27 2018 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-16
- Restore libstdc++ patch.
- Update udev rules.
- Remove obsolete scriptlets.

* Mon Mar 26 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0.54-15
- Switch to libva with f28+

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0.0.54-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-13
- Do not require libtxc_dxtn on Fedora 26+.

* Thu Nov 16 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-12
- Do not require libtxc_dxtn on Fedora 28+ (Mesa 17.3.0+).
- Update udev rules.

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.0.54-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 08 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-10
- Require alsa-plugins-pulseaudio and libatomic.

* Wed Apr 19 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-9
- GTK 2/3 version of libdbusmenu at version 16.04.0 is required for a working
  tray menu depending on the desktop.

* Mon Apr 10 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-8
- Update udev rules.

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.0.54-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Feb 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-6
- Remove libstdc++ patch.
- Update udev rules.
- Update docs for hardware encoding/decoding information.

* Fri Feb 10 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-5
- Remove noruntime subpackage, use default new mechanism that uses host
  libraries as per client update of 19th January (5th January for beta):
  http://store.steampowered.com/news/26953/
- Add libdbusmenu-gtk3 library requirement on Fedora (luckily not RHEL/CentOS).
- Remove patch for window button behaviour, use shell profile.

* Sun Jan 22 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-4
- Fix Source URL for post kernel 4.9 udev rules.
- Reintroduce optional and not endorsed by Valve noruntime subpackage for using
  all system libraries in place of all the Ubuntu runtime ones.

* Sun Jan 08 2017 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-3
- Microsoft keyboards have been fixed in kernel 4.9 and backported to other
  kernels.

* Tue Dec 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-2
- Re-add close functionality to X window button (#3210).

* Thu Dec 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.54-1
- Update to 1.0.0.54.
- Update udev patch.

* Wed Oct 26 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.53-1
- Update to 1.0.0.53.
- Update udev rules.

* Sat Sep 24 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.52-3
- Do not run update-desktop-database on Fedora 25+.
- Add AppStream metadata.

* Sat Aug 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.52-2
- Make Steam Controller usable as a gamepad (#4062).
- Update UDev rule for keyboards detected as joysticks.
- Update README.Fedora file with notes about the Steam Controller, its update
  process and update the list of devices with UDev rules.

* Fri Apr 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.52-1
- Update to 1.0.0.52, adds HTC Vive udev rules.
- Update patches.

* Thu Feb 25 2016 Simone Caronni <negativo17@gmail.com> - 1.0.0.51-2
- Integrate FirewallD rules (still not enabled by default).
- Add support for Nvidia Shield Controller.
- Add UDev rules for keyboards detected as joysticks:
  https://github.com/ValveSoftware/steam-for-linux/issues/3384
  https://bugzilla.kernel.org/show_bug.cgi?id=28912
  https://github.com/denilsonsa/udev-joystick-blacklist
- Update README.Fedora accordingly.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.51-1
- Update to 1.0.0.51.
- Add dependencies for In-Home Streaming decoding.
- Updated udev rules for the Steam Controller and HTC Vive VR headset.
- Update isa requirements.

* Mon May 25 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.50-2
- Add license macro.
- Add workaround for bug 3273, required for running client/games with prime:
  https://github.com/ValveSoftware/steam-for-linux/issues/3273

* Thu May 07 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.50-1
- Update to 1.0.0.50.
- Add new requirements; update README file.

* Mon Jan 12 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-4
- Flash plugin is no longer required for playing videos in the store, update
  README.Fedora.

* Thu Jan 08 2015 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-3
- Workaround for bug 3570:
  https://github.com/ValveSoftware/steam-for-linux/issues/3570

* Tue Dec 02 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-2
- Update requirements.

* Wed Aug 27 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.49-1
- Update to 1.0.0.49.

* Tue Jul 29 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.48-3
- Obsolete noruntime subpackage.

* Mon Jun 23 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.48-2
- Add additional libraries required by games when skipping runtime.

* Thu Jun 19 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.48-1
- Update to 1.0.0.48.

* Thu May 15 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-4
- Update noruntime subpackage requirements.

* Mon May 05 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-3
- Add new libbz2.so requirement.

* Tue Apr 01 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-2
- Close window when clicking the x button (#3210).

* Wed Feb 12 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.47-1
- Update to 1.0.0.47.

* Mon Jan 06 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-6
- Make noruntime subpackage noarch.

* Mon Jan 06 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-5
- Update README.Fedora with new instructions.

* Mon Jan 06 2014 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-4
- Create a no-runtime subpackage leaving the main package to behave as intended
  by Valve. All the Steam Runtime dependencies are against the subpackage.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-3
- Additional system libraries required by games.

* Fri Dec 20 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-2
- If STEAM_RUNTIME is not set, perform the following actions by default from the
  main commmand:
    Disable the Ubuntu runtime.
    Delete the unpacked Ubuntu runtime.
    Create the obsolete libudev.so.0.

* Wed Nov 27 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.45-1
- Update to 1.0.0.45.

* Thu Nov 14 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.44-1
- Update to 1.0.0.44.

* Fri Nov 08 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-9
- Disable STEAM_RUNTIME, drop all requirements and change README.Fedora. Please
  see for details:
    https://github.com/ValveSoftware/steam-for-linux/issues/2972
    https://github.com/ValveSoftware/steam-for-linux/issues/2976
    https://github.com/ValveSoftware/steam-for-linux/issues/2978

* Mon Nov 04 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-8
- Add missing mesa-dri-drivers requirement.

* Mon Oct 28 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-7
- Added libXScrnSaver to requirements.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-6
- Rpmlint review fixes.

* Wed Oct 23 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-5
- Do not remove buildroot in install section.
- Update desktop database after installation/uninstallation.

* Tue Oct 22 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-4
- Added systemd build requirement for udev rules.

* Sun Oct 20 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-3
- Add alsa-plugins-pulseaudio to requirements.
- Add libappindicator to requirements to enable system tray icon.

* Thu Oct 10 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-2
- Remove requirements pulled in by other components.

* Wed Oct 09 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.43-1
- Update to 1.0.0.43.

* Thu Oct 03 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.42-2
- Remove rpmfusion repository dependency.

* Wed Sep 11 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.42-1
- Update to 1.0.0.42.

* Sun Sep 08 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.41-1
- Update to 1.0.0.41.

* Thu Aug 29 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.40-1
- Update to 1.0.0.40.
- Add Steam controller support.

* Sun Aug 18 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-5
- Rework requirements section.
- Add tar and zenity requirements for initial setup.

* Mon Aug 05 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-4
- Remove Fedora 17 as it is now EOL.

* Wed May 29 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-3
- Add STEAM_RUNTIME=0 to profile settings.

* Mon May 13 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-2
- Added NetworkManager requirement for STEAM_RUNTIME=0.

* Mon May 13 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.39-1
- Updated to 1.0.0.39.

* Thu May 09 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.38-2
- Changed Fedora 19 FLAC requirements.

* Sun Apr 28 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.38-1
- Updated to 1.0.0.38.

* Fri Apr 19 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.36-2
- Add additional libraries for starting with STEAM_RUNTIME=0.
- Added README.Fedora document with additional instructions.

* Fri Mar 15 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.36-1
- Update to 1.0.0.36.

* Mon Mar 04 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.35-1
- Updated.

* Mon Feb 25 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.34-1
- Update to 1.0.0.34.

* Thu Feb 21 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.29-2
- Added changelog to docs.

* Thu Feb 21 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.29-1
- Updated.

* Fri Feb 15 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.27-1
- Updated, used official install script.
- Removed patch.

* Mon Feb 11 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.25-1
- Updated to 1.0.0.25.
- Reworked installation for new tar package.
- Used official docs.

* Tue Jan 22 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.22-3
- Moved documents to the default document directory.
- Use internal license file instead of provided one.
- Removed STEAMSCRIPT modification, fixed in 1.0.0.22.

* Tue Jan 22 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.22-1
- Updated.

* Thu Jan 17 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.21-2
- Sorted Requires.
- Fix STEAMSCRIPT_VERSION.
- Added RPMFusion free repository as requirement for libtxc_dxtn (or nvidia drivers...).

* Thu Jan 17 2013 Simone Caronni <negativo17@gmail.com> - 1.0.0.21-1
- Updated version, patch and tarball generation for 1.0.0.21.
- Added libtxc_dxtn requirement (rpmfusion).
- Replaced steam with %%{name} where it fits.
- Removed jpeg library hack.
- Removed SDL2 requirement, is downloaded by the client.
- Replace (x86-32) with %%{_isa}.

* Tue Jan 8 2013 Tom Callaway <spot@fedoraproject.org> - 1.0.0.18-1
- update to 1.0.0.18

* Wed Nov 7 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0.14-3
- add more Requires (from downloaded bits, not packaged bits)

* Tue Nov 6 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0.14-2
- fedora specific libpng conditionalization

* Tue Nov 6 2012 Tom Callaway <spot@fedoraproject.org> - 1.0.0.14-1
- initial Fedora RPM packaging
