%global debug_package %{nil}
%global appstream_id com.valvesoftware.Steam

Name:           steam
Version:        1.0.0.87
Release:        2%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file
License:        Steam License Agreement
URL:            http://www.steampowered.com/
ExclusiveArch:  x86_64

Source0:        https://repo.steampowered.com/%{name}/archive/beta/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source3:        README.Fedora
# Configure limits in systemd
Source7:        01-steam.conf

# Do not install desktop file in lib/steam, do not install apt sources
Patch0:         %{name}-makefile.patch
# Do not try to copy steam.desktop to the user's desktop from lib/steam
Patch1:         %{name}-no-icon-on-desktop.patch

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  systemd

# Required for the basic runtime
Requires:       glibc(x86-32)
Requires:       libdrm(x86-32)
Requires:       libglvnd-glx(x86-32)
Requires:       libnsl(x86-32)

# Required to run the initial setup
Requires:       tar
Requires:       zenity
Requires:       xz

# Required for basic gaming, also for native 32 bit games:
Requires:       mesa-dri-drivers
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-vulkan-drivers
Requires:       mesa-vulkan-drivers(x86-32)
Requires:       vulkan-loader
Requires:       vulkan-loader(x86-32)

# Hardware stuff (permissions on devices, hardware updater, etc.):
Requires:       steam-devices

# These libraries are also part of the Ubuntu runtime at:
#   ~/.local/share/Steam/ubuntu12_32
#   ~/.local/share/Steam/ubuntu12_64
# Steam client uses the system ones if available; so override where there is a
# benefit using the native system libaries or just to match when the native 64
# bit packages are already installed.
Requires:       bzip2-libs
Requires:       bzip2-libs(x86-32)
Requires:       fontconfig
Requires:       fontconfig(x86-32)
Requires:       libICE
Requires:       libICE(x86-32)
Requires:       libnsl
Requires:       libnsl(x86-32)
Requires:       libXext
Requires:       libXext(x86-32)
Requires:       libXinerama
Requires:       libXinerama(x86-32)
Requires:       libXtst
Requires:       libXtst(x86-32)
Requires:       libva
Requires:       libva(x86-32)
Requires:       libvdpau
Requires:       libvdpau(x86-32)
Requires:       mesa-libGL
Requires:       mesa-libGL(x86-32)
Requires:       NetworkManager-libnm
Requires:       NetworkManager-libnm(x86-32)
Requires:       nss
Requires:       nss(x86-32)
Requires:       openal-soft
Requires:       openal-soft(x86-32)
Requires:       pipewire-libs
Requires:       pipewire-libs(x86-32)
Requires:       pulseaudio-libs
Requires:       pulseaudio-libs(x86-32)
%if 0%{?fedora} || 0%{?rhel} >= 10
Requires:       SDL3
Requires:       SDL3(x86-32)
%endif
# The client does not override only the ones linked at:
#   ~/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_32
#   ~/.local/share/Steam/ubuntu12_32/steam-runtime/pinned_libs_64
# At the moment of writing, the pinned ones belong to these packages:
#   gtk2
#   libcurl
#   libdbusmenu
#   libdbusmenu-gtk2
#   mesa-libGLU
# And yes, the "ubuntu12_32" directory twice above is not a typo. Windows style (system32...).

# Required for the firewall rules
# http://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem

# Required by Feral interactive games
Requires:       libatomic
Requires:       libatomic(x86-32)

# Required by Shank
Requires:       (alsa-plugins-pulseaudio if pulseaudio)

# Game performance is increased with gamemode (for games that support it)
Recommends:     gamemode
Recommends:     (gnome-shell-extension-appindicator if gnome-shell)

# Proton uses xdg-desktop-portal to open URLs from inside a container
Requires:       xdg-desktop-portal
Recommends:     (xdg-desktop-portal-gtk if gnome-shell)
Recommends:     (xdg-desktop-portal-kde if kwin)

# Prevent log spam when thse are not pulled in as dependencies of full desktops
Recommends:     dbus-x11
Recommends:     xdg-user-dirs

# Allow using Steam Runtime Launch Options
Recommends:     gobject-introspection

# Automatic loading of the ntsync module
Recommends:     ntsync-autoload

%description
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the installer for the Steam software distribution service.

%package arch-transition
Summary: Transition package for migrating Steam from i686 to x86_64
Requires: %{name} = %{version}-%{release}
Provides: steam = 1.0.0.85-8
Obsoletes: steam < 1.0.0.85-8
BuildArch: noarch

%description arch-transition
This package is used to migrate Steam installations from the
legacy i686 package layout to the x86_64 package layout.

It exists only to handle package replacement and dependency
changes during upgrades, and can be safely removed once the
transition is complete.

%prep
%autosetup -p1 -n %{name}-launcher

cp %{SOURCE3} .

%build
# Nothing to build

%install
%make_install

rm -fr \
    %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

# Environment files
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

# Raise file descriptor limit
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/user.conf.d/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%license COPYING steam_subscriber_agreement.txt
%doc debian/changelog README.Fedora
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_prefix}/lib/%{name}/
%{_mandir}/man6/%{name}.*
%{_metainfodir}/%{appstream_id}.metainfo.xml
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%dir %{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%dir %{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf

%files arch-transition

%changelog
* Sun Aug 02 2026 RPM Fusion Release Engineering <leigh123linux@rpmfusion.org> - 1.0.0.87-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Fri Jul 03 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.87-1
- Update to 1.0.0.87.

* Fri Jun 19 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.86-1
- Update to 1.0.0.86.

* Sun May 31 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-10
- Latest client statically links libhidapi where required.

* Tue May 26 2026 Sérgio Basto <sergio@serjux.com> - 1.0.0.85-9
- Add steam-arch-transition package for i686 to x86_64 migration

* Thu May 21 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-8
- RHEL does not have SDL3 packages, and the client is all SDL3 based.

* Wed May 20 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-7
- Package is now x86_64 as the client itself is all 64 bit based.
- Most of the client libraries are also installed in 32 bit format, as all the
  client features compiled into the games still require them. For the same
  reason, 32 bit graphics libraries are also required.
- Override client libraries using system ones where it makes sense.
- Recommends hidapi for the the new hardware updater (#7452) until a new stable
  client release lands.
- Trim changelog.

* Mon Apr 13 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-6
- Drop certificate workaround:
  https://bodhi.fedoraproject.org/updates/FEDORA-2026-285c6d38f7

* Mon Mar 23 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-5
- Convert certificates workaround to trigger.

* Thu Feb 19 2026 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-4
- Apply workaround for
  https://fedoraproject.org/wiki/Changes/droppingOfCertPemFile.

* Mon Feb 02 2026 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.85-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Nov 26 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-2
- Do not provide ntsync loading mechanism, require the ntsync-autoload package
  (ntsync is not yet enabled in official Proton versions).

* Fri Oct 17 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-1
- Update to 1.0.0.85.

* Sat Sep 06 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.83-3
- Load ntsync module.

* Mon Jul 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun May 11 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.83-1
- Update to 1.0.0.83.

* Wed Apr 09 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.82-4
- Drop steam-devices subpackage.

* Wed Mar 19 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.82-3
- Relax requirement on steam-devices.
- Trim changelog.
- Update README.

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
