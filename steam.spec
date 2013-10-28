# Binary package, no debuginfo should be generated
%global debug_package %{nil}

Name:           steam
Version:        1.0.0.43
Release:        7%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file
License:        Steam License Agreement   
URL:            http://www.steampowered.com/
Source0:        http://repo.steampowered.com/steam/pool/%{name}/s/%{name}/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source10:       README.Fedora
ExclusiveArch:  i686

BuildRequires:  desktop-file-utils
BuildRequires:  systemd

# Required to run the initial setup
Requires:       tar
Requires:       zenity
# Required for S3 compressed textures on free drivers
Requires:       libtxc_dxtn%{_isa}
# Required for enabling Steam system tray icon
Requires:       libappindicator%{_isa}

# After the Steam client has been downloaded run the following command and then
# adjust the list of requirements to remove dependencies pulled in by other
# packages.

# cd ~/.local/share/Steam/ubuntu12_32/
# for i in `ldd *.so | egrep -v "linux-gate.so|ld-linux.so" | awk '{print $1}'`; do
#   repoquery --disablerepo=* --enablerepo=fedora,updates -q --qf="Requires:       %%{name}" --whatprovides "$i"
# done | sort | uniq | sed 's/$/%%{_isa}/g'

Requires:       alsa-lib%{_isa}
Requires:       alsa-plugins-pulseaudio%{_isa}
Requires:       avahi-libs%{_isa}
Requires:       expat%{_isa}
Requires:       gtk2%{_isa}
Requires:       harfbuzz%{_isa}
Requires:       json-c%{_isa}
Requires:       keyutils-libs%{_isa}
Requires:       libasyncns%{_isa}
Requires:       libattr%{_isa}
Requires:       libffi%{_isa}
Requires:       libpng12%{_isa}
Requires:       libsndfile%{_isa}
Requires:       libusbx%{_isa}
Requires:       libXau%{_isa}
Requires:       libXdmcp%{_isa}
Requires:       libXScrnSaver%{_isa}
Requires:       mesa-libEGL%{_isa}
Requires:       mesa-libgbm%{_isa}
Requires:       mesa-libGL%{_isa}
Requires:       NetworkManager-glib%{_isa}
Requires:       nss%{_isa}
Requires:       openal-soft%{_isa}
Requires:       openssl-libs%{_isa}
Requires:       pcre%{_isa}
Requires:       pixman%{_isa}
Requires:       pulseaudio-libs%{_isa}
Requires:       tcp_wrappers-libs%{_isa}

%if 0%{?fedora} >= 19
# SDL2 it's already bundled in the Steam client but cannot be removed (it's not
# in the runtime). Leave it here as this will probably not be shipped for long.
Requires:       SDL2%{_isa}
%endif

%description
Installer for the Steam software distribution service.
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized
savegame and screenshot functionality, and many social features.

%prep
%setup -q -n %{name}
sed -i 's/\r$//' %{name}.desktop
sed -i 's/\r$//' steam_install_agreement.txt
cp %{SOURCE10} .

%build
# Nothing to build

%install
make install DESTDIR=%{buildroot}
rm -fr %{buildroot}%{_docdir}/%{name}/ %{buildroot}%{_bindir}/%{name}deps

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

install -D -m 644 -p lib/udev/rules.d/99-steam-controller-perms.rules \
    %{buildroot}%{_udevrulesdir}/99-steam-controller-perms.rules

mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

%files
%doc README COPYING steam_install_agreement.txt debian/changelog README.Fedora
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_udevrulesdir}/99-steam-controller-perms.rules

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%{_bindir}/update-desktop-database &> /dev/null || :

%postun
%{_bindir}/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    %{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
%{_bindir}/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%changelog
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
