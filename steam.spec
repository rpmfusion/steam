# Binary package, no debuginfo should be generated
%global debug_package %{nil}

Name:           steam
Version:        1.0.0.51
Release:        1%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file
License:        Steam License Agreement
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        http://repo.steampowered.com/steam/pool/%{name}/s/%{name}/%{name}_%{version}.tar.gz
Source3:        %{name}.xml
Source10:       README.Fedora
Patch0:         %{name}-3570.patch
Patch1:         %{name}-3273.patch

BuildRequires:  desktop-file-utils
BuildRequires:  systemd

# Required to run the initial setup
Requires:       tar
Requires:       zenity
# Required for S3 compressed textures on free drivers
Requires:       libtxc_dxtn%{?_isa}
# Required for running the package on 32 bit systems with free drivers
Requires:       mesa-dri-drivers%{?_isa}
# Minimum requirements for starting the steam client for the first time
Requires:       alsa-lib%{?_isa}
Requires:       gtk2%{?_isa}
Requires:       libpng12%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXinerama%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       mesa-libGL%{?_isa}
Requires:       nss%{?_isa}
# Required for sending out crash reports to Valve
Requires:       libcurl%{?_isa}
# Workaround for mesa-libGL dependency bug:
# https://bugzilla.redhat.com/show_bug.cgi?id=1168475
Requires:       systemd-libs%{?_isa}

# Required for hardware decoding during In-Home Streaming (intel)
Requires:       libva-intel-driver%{?_isa}

# Required for hardware decoding during In-Home Streaming (radeon/nouveau)
Requires:       libvdpau%{?_isa}

Obsoletes:      %{name}-noruntime < %{version}-%{release}
Provides:       %{name}-noruntime = %{version}-%{release}

%description
Installer for the Steam software distribution service.
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized
savegame and screenshot functionality, and many social features.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
sed -i 's/\r$//' %{name}.desktop
sed -i 's/\r$//' steam_install_agreement.txt
cp %{SOURCE10} .

%build
# Nothing to build

%install
%make_install
rm -fr %{buildroot}%{_docdir}/%{name}/ %{buildroot}%{_bindir}/%{name}deps

desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

install -D -m 644 -p lib/udev/rules.d/99-steam-controller-perms.rules \
    %{buildroot}%{_udevrulesdir}/99-steam-controller-perms.rules

install -D -m 644 -p %{SOURCE3} \
    %{buildroot}%{_prefix}/lib/firewalld/services/steam.xml

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

%files
%{!?_licensedir:%global license %%doc}
%license COPYING steam_install_agreement.txt
%doc README debian/changelog README.Fedora
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_udevrulesdir}/99-steam-controller-perms.rules

%changelog
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
