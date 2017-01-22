# Binary package, no debuginfo should be generated
%global debug_package %{nil}

# If firewalld macro is not defined, define it here:
%{!?firewalld_reload:%global firewalld_reload test -f /usr/bin/firewall-cmd && firewall-cmd --reload --quiet || :}

Name:           steam
Version:        1.0.0.54
Release:        4%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file
License:        Steam License Agreement
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        http://repo.steampowered.com/steam/pool/%{name}/s/%{name}/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source3:        %{name}.xml
Source4:        %{name}.appdata.xml

# Workaround for input devices seen as joysticks (linux kernel bug) and
# viceversa for the Steam controller:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist
#
# Microsoft patch accepted upstream, remove Microsoft entries when kernel
# is at 4.9: https://bugzilla.redhat.com/show_bug.cgi?id=1325354#c14
Source8:        https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/after_kernel_4_9/51-these-are-not-joysticks-rm.rules
Source9:        https://raw.githubusercontent.com/cyndis/shield-controller-config/master/99-shield-controller.rules

Source10:       README.Fedora

# Remove temporary leftover files after run (fixes multiuser):
# https://github.com/ValveSoftware/steam-for-linux/issues/3570
Patch0:         %{name}-3570.patch

# Remove libstdc++ from runtime on systems where mesa is compiled normally
# (RHEL 7). Fixes crash:
# https://github.com/ValveSoftware/steam-for-linux/issues/3273
Patch1:         %{name}-3273.patch

# Make Steam Controller usable as a GamePad:
# https://steamcommunity.com/app/353370/discussions/0/490123197956024380/
Patch2:         %{name}-controller-gamepad-emulation.patch

# Make "X" window button close the program instead of minimizing like "_"
Patch3:         %{name}-3210.patch

# Do not remove libstdc++ from runtime on systems where mesa is compiled with
# a statically linked libstdc++ (Fedora 22+) and enable option to run without
# Ubuntu runtime:
# https://github.com/ValveSoftware/steam-for-linux/issues/3697
Patch4:         %{name}-disable-runtime.patch

BuildRequires:  desktop-file-utils
BuildRequires:  systemd

# Required to run the initial setup
Requires:       tar
Requires:       zenity

# Required for S3 compressed textures on free drivers (intel/radeon/nouveau)
Requires:       libtxc_dxtn%{?_isa}

# Required for running the package on 32 bit systems with free drivers
Requires:       mesa-dri-drivers%{?_isa}

# Minimum requirements for starting the steam client for the first time
Requires:       alsa-lib%{?_isa}
Requires:       gtk2%{?_isa}
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
%if 0%{?rhel}
Requires:       firewalld
Requires(post): firewalld
%else
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
%endif

# Required for hardware decoding during In-Home Streaming (intel)
Requires:       libva-intel-driver%{?_isa}

# Required for hardware decoding during In-Home Streaming (radeon/nouveau)
Requires:       libvdpau%{?_isa}

%description
Installer for the Steam software distribution service.
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized
savegame and screenshot functionality, and many social features.

%if !0%{?rhel}
%package        noruntime
Summary:        Use system libraries instead of the Steam Runtime
Requires:       steam = %{version}-%{release}
Buildarch:      noarch

# After the Steam client has been downloaded once, run the following command and
# then adjust the list of requirements to remove dependencies pulled in by other
# packages.

# cd ~/.local/share/Steam/ubuntu12_32/
# for i in `ldd *.so | egrep -v "linux-gate.so|ld-linux.so" | awk '{print $1}'` `find steam-runtime/i386 -name "*.so*" -exec basename {} \;`; do
#   dnf repoquery -q --qf="Requires:       %{name}" --whatprovides "$i"
# done | sort | uniq | sed 's/$/%{?_isa}/g'

# Then remove compiz and emerald.

Requires:       alsa-lib%{?_isa}
Requires:       alsa-plugins-arcamav%{?_isa}
Requires:       alsa-plugins-jack%{?_isa}
Requires:       alsa-plugins-oss%{?_isa}
Requires:       alsa-plugins-pulseaudio%{?_isa}
Requires:       alsa-plugins-samplerate%{?_isa}
Requires:       alsa-plugins-speex%{?_isa}
Requires:       alsa-plugins-upmix%{?_isa}
Requires:       alsa-plugins-usbstream%{?_isa}
Requires:       alsa-plugins-vdownmix%{?_isa}
Requires:       atk%{?_isa}
Requires:       avahi-libs%{?_isa}
Requires:       bzip2-libs%{?_isa}
Requires:       cairo%{?_isa}
Requires:       compat-libgcrypt%{?_isa}
Requires:       cups-libs%{?_isa}
Requires:       dbus-glib%{?_isa}
Requires:       dbus-libs%{?_isa}
Requires:       dconf%{?_isa}
Requires:       elfutils-libelf%{?_isa}
Requires:       elfutils-libs%{?_isa}
Requires:       expat%{?_isa}
Requires:       ffmpeg-libs%{?_isa}
Requires:       flac-libs%{?_isa}
Requires:       fontconfig%{?_isa}
Requires:       freeglut%{?_isa}
Requires:       freetype%{?_isa}
Requires:       GConf2%{?_isa}
Requires:       gdk-pixbuf2%{?_isa}
Requires:       glib2%{?_isa}
Requires:       glibc%{?_isa}
Requires:       gmp%{?_isa}
Requires:       gnutls%{?_isa}
Requires:       graphite2%{?_isa}
Requires:       gsm%{?_isa}
Requires:       gstreamer%{?_isa}
Requires:       gstreamer1%{?_isa}
Requires:       gstreamer-devel%{?_isa}
Requires:       gstreamer-plugins-base%{?_isa}
Requires:       gtk2%{?_isa}
Requires:       gtk2-engines%{?_isa}
Requires:       gtk3%{?_isa}
Requires:       gtk-murrine-engine%{?_isa}
Requires:       harfbuzz%{?_isa}
Requires:       heimdal-libs%{?_isa}
Requires:       jack-audio-connection-kit%{?_isa}
Requires:       json-c%{?_isa}
Requires:       keyutils-libs%{?_isa}
Requires:       krb5-libs%{?_isa}
Requires:       lcms2%{?_isa}
Requires:       libacl%{?_isa}
Requires:       libappindicator%{?_isa}
Requires:       libasyncns%{?_isa}
Requires:       libattr%{?_isa}
Requires:       libcanberra%{?_isa}
Requires:       libcanberra-gtk2%{?_isa}
Requires:       libcap%{?_isa}
Requires:       libcom_err%{?_isa}
Requires:       libcurl%{?_isa}
Requires:       libdbusmenu%{?_isa}
Requires:       libdbusmenu-gtk2%{?_isa}
Requires:       libdrm%{?_isa}
Requires:       libexif%{?_isa}
Requires:       libffi%{?_isa}
Requires:       libgcc%{?_isa}
Requires:       libgcrypt%{?_isa}
Requires:       libGLEW%{?_isa}
Requires:       libgomp%{?_isa}
Requires:       libgpg-error%{?_isa}
Requires:       libICE%{?_isa}
Requires:       libidn%{?_isa}
Requires:       libindicator%{?_isa}
Requires:       libjpeg-turbo%{?_isa}
Requires:       libnotify%{?_isa}
Requires:       libogg%{?_isa}
Requires:       libpng%{?_isa}
Requires:       libpng12%{?_isa}
Requires:       libsamplerate%{?_isa}
Requires:       libselinux%{?_isa}
Requires:       libSM%{?_isa}
Requires:       libsndfile%{?_isa}
Requires:       libstdc++%{?_isa}
Requires:       libtasn1%{?_isa}
Requires:       libtdb%{?_isa}
Requires:       libtheora%{?_isa}
Requires:       libtool-ltdl%{?_isa}
Requires:       libusbx%{?_isa}
Requires:       libuuid%{?_isa}
Requires:       libva%{?_isa}
Requires:       libvdpau%{?_isa}
Requires:       libvorbis%{?_isa}
Requires:       libvpx%{?_isa}
Requires:       libwayland-client%{?_isa}
Requires:       libwayland-server%{?_isa}
Requires:       libX11%{?_isa}
Requires:       libXau%{?_isa}
Requires:       libXaw%{?_isa}
Requires:       libxcb%{?_isa}
Requires:       libXcomposite%{?_isa}
Requires:       libXcursor%{?_isa}
Requires:       libXdamage%{?_isa}
Requires:       libXdmcp%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXfixes%{?_isa}
Requires:       libXft%{?_isa}
Requires:       libXi%{?_isa}
Requires:       libXinerama%{?_isa}
Requires:       libxml2%{?_isa}
Requires:       libXmu%{?_isa}
Requires:       libXpm%{?_isa}
Requires:       libXrandr%{?_isa}
Requires:       libXrender%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       libxshmfence%{?_isa}
Requires:       libXt%{?_isa}
Requires:       libXtst%{?_isa}
Requires:       libXxf86vm%{?_isa}
Requires:       mesa-libEGL%{?_isa}
Requires:       mesa-libgbm%{?_isa}
Requires:       mesa-libGL%{?_isa}
Requires:       mesa-libglapi%{?_isa}
Requires:       mesa-libGLU%{?_isa}
Requires:       ncurses-libs%{?_isa}
Requires:       nettle%{?_isa}
Requires:       NetworkManager-glib%{?_isa}
Requires:       nspr%{?_isa}
Requires:       nss%{?_isa}
Requires:       nss-softokn%{?_isa}
Requires:       nss-softokn-freebl%{?_isa}
Requires:       nss-util%{?_isa}
Requires:       openal-soft%{?_isa}
Requires:       openldap%{?_isa}
Requires:       openssl-libs%{?_isa}
Requires:       orc%{?_isa}
Requires:       p11-kit%{?_isa}
Requires:       pango%{?_isa}
Requires:       pangox-compat%{?_isa}
Requires:       pciutils-libs%{?_isa}
Requires:       pcre%{?_isa}
Requires:       pixman%{?_isa}
Requires:       pulseaudio-libs%{?_isa}
Requires:       SDL%{?_isa}
Requires:       SDL2%{?_isa}
Requires:       SDL2_image%{?_isa}
Requires:       SDL2_mixer%{?_isa}
Requires:       SDL2_net%{?_isa}
Requires:       SDL2_ttf%{?_isa}
Requires:       SDL_image%{?_isa}
Requires:       SDL_mixer%{?_isa}
Requires:       SDL_ttf%{?_isa}
Requires:       speex%{?_isa}
Requires:       speexdsp%{?_isa}
Requires:       sqlite%{?_isa}
Requires:       systemd-libs%{?_isa}
Requires:       tbb%{?_isa}
Requires:       tcp_wrappers-libs%{?_isa}
Requires:       xz-libs%{?_isa}
Requires:       zlib%{?_isa}

%if 0%{?fedora} >= 23
Requires:       libgudev%{?_isa}
Requires:       trousers-lib%{?_isa}
%else
Requires:       libgudev1%{?_isa}
Requires:       trousers%{?_isa}
%endif

%description    noruntime
The Steam client normally uses a set of libraries derived from Ubuntu (the Steam
Runtime); and all titles on Steam are compiled against those libraries.

This package takes care of installing all the requirements to use system
libraries in place of the Steam Runtime and a profile environment file to enable
it. Please note that this is not a supported Valve configuration and it may lead
to unexpected results.
%endif

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%if !0%{?rhel}
# Steam no-runtime package
%patch4 -p1
%endif

sed -i 's/\r$//' %{name}.desktop
sed -i 's/\r$//' steam_install_agreement.txt

cp %{SOURCE10} .

%build
# Nothing to build

%install
%make_install

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

mkdir -p %{buildroot}%{_udevrulesdir}/
install -m 644 -p lib/udev/rules.d/* \
    %{SOURCE8} %{SOURCE9} %{buildroot}%{_udevrulesdir}/

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

install -D -m 644 -p %{SOURCE3} \
    %{buildroot}%{_prefix}/lib/firewalld/services/steam.xml

%if !0%{?rhel}
# Steam no-runtime package
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d
%endif

%if 0%{?fedora} >= 25
# Install AppData
mkdir -p %{buildroot}%{_datadir}/appdata
install -p -m 0644 %{SOURCE4} %{buildroot}%{_datadir}/appdata/
%endif

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel} == 7
/usr/bin/update-desktop-database &> /dev/null || :
%endif
%firewalld_reload

%postun
%if 0%{?fedora} == 24 || 0%{?fedora} == 23 || 0%{?rhel} == 7
/usr/bin/update-desktop-database &> /dev/null || :
%endif
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%{!?_licensedir:%global license %%doc}
%license COPYING steam_install_agreement.txt
%doc README debian/changelog README.Fedora
%{_bindir}/%{name}
%if 0%{?fedora} >= 25
%{_datadir}/appdata/%{name}.appdata.xml
%endif
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_udevrulesdir}/*

%if !0%{?rhel}
%files noruntime
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%endif

%changelog
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
