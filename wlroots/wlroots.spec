%global commit  0.12.0
%global gitdate %{nil}
%global gitrel  %{nil}
%global gitver  %{nil}
# Keep the below around for possible snapshot times (was a must prior to 0.1)
#global scommit #(c=#{commit}; echo ${c:0:7})
#global gitrel  .#{gitdate}git#{scommit}
#global gitver  -#{gitdate}git#{scommit}


%global api_ver 7


Name:           wlroots
Version:        %{commit}
Release:        1%{?gitrel}%{?dist}
Summary:        A modular Wayland compositor library

# Source files/overall project licensed as MIT, but
# - LGPLv2.1+
#   * protocol/idle.xml
#   * protocol/server-decoration.xml
# Those files are processed to C-compilable files by the
# `wayland-scanner` binary during build and don't alter
# the main license of the binaries linking with them by
# the underlying licenses.

License:        MIT
URL:            https://github.com/swaywm/%{name}
Source0:        %{url}/archive/%{commit}.tar.gz#/%{name}-%{version}%{?gitver}.tar.gz
# this file is a modification of examples/meson.build so as to:
# - make it self-contained
# - only has targets for examples known to compile well (cf. "examples) global)
Source1:        examples.meson.build

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  meson >= 0.48.0
# patch application
#BuildRequires:  git

BuildRequires:  pkgconfig(freerdp2)
#                                   freerdp-devel
BuildRequires:  pkgconfig(libcap)
#                                   libcap-devel
BuildRequires:  pkgconfig(libdrm) >= 2.4.95
#                                   libdrm-devel >= 2.4.95
#                                   # transitively: mesa-libEGL-devel
BuildRequires:  pkgconfig(libinput) >= 1.9.0
#                                   libinput-devel >= 1.9.0
BuildRequires:  pkgconfig(winpr2)
#                                   libwinpr-devel
BuildRequires:  pkgconfig(xkbcommon)
#                                   libxkbcommon-devel
#                                   # transitively: freerdp-devel
BuildRequires:  pkgconfig(egl)
#                                   mesa-libEGL-devel
BuildRequires:  mesa-libEGL-devel
# ^^^ because in f32 ^^^ lost pkgconfig(egl) provides :(
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(gbm) >= 17.1.0
#                                   mesa-libgbm-devel >= 17.1.0
BuildRequires:  pkgconfig(pixman-1)
#                                   pixman-devel
BuildRequires:  pkgconfig(libudev)
#                                   systemd-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server) >= 1.16
#                                   wayland-devel >= 1.16
#                                   # transitively: freerdp-devel
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
#                                   wayland-protocols-devel >= 1.17
BuildRequires:  pkgconfig(xcb-icccm)
#                                   xcb-util-wm-devel

# these are for examples only:
#BuildRequires: pkgconfig(libpng)
#                                   libpng
#                                   for: examples/screencopy
#BuildRequires: libavcoded libavformat libavutil
#                                   not in Fedora
#                                   for: examples/dmabuf-capture


# only select examples are supported for being readily compilable (see SOURCE1)
%global examples %{nil \
} cat multi-pointer output-layout pointer rotation screencopy simple tablet touch


%description
%{summary}.


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} == %{version}-%{release}
Requires:       xcb-util-wm-devel%{?_isa}
# these dependencies are fulfilled with automatic "pkgconfig(*)")
#Requires:       libinput-devel#{?_isa} >= 1.9.0
#Requires:       libxkbcommon-devel${?_isa}
#Requires:       mesa-libEGL-devel${?_isa}
#Requires:       pixman-devel#{?_isa}
#Requires:       systemd-devel#{?_isa}
#Requires:       wayland-devel#{?_isa} >= 1.16

# for examples
Suggests:       gcc
Suggests:       libpng
Suggests:       meson

%description    devel
Development files for %{name}.


%prep
%autosetup -p1 -n %{name}-%{commit}
#global __scm git_am
#__scm_setup_git
#autopatch -p1


%build

# Needed since xcb-errors is not packaged (yet?)
%global __meson_auto_features auto
%meson -Drootston=false -Dexamples=false
%meson_build


%install
%meson_install

# %%doc && examples.
%{__mkdir} -p %{buildroot}%{_pkgdocdir}/examples
%{__cp} -p README.md %{buildroot}%{_pkgdocdir}
examples=$(for e in %{examples}; do echo examples/$e.[ch]; done)
%{__cp} -p ${examples} %{buildroot}%{_pkgdocdir}/examples
%{__cp} -p %SOURCE1 %{buildroot}%{_pkgdocdir}/examples/meson.build


%check
%meson_test


%files
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%license LICENSE
%{_libdir}/lib%{name}.so.%{api_ver}*


%files          devel
%doc %{_pkgdocdir}/examples
%{_includedir}/wlr
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Thu Aug 29 2019 Jeff Peeler <jpeeler@redhat.com> - 0.7.0-1
- Updated to version 0.7.0

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Jan Pokorný <jpokorny+rpm-wlroots@fedoraproject.org> - 0.6.0-1
- Updated to version 0.6.0
  (see https://github.com/swaywm/wlroots/releases/tag/0.6.0)
- Overhaul dependencies and shipped examples in -devel

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 0.5.0-2
- Rebuild with Meson fix for #1699099

* Thu Mar 14 2019 Jan Pokorný <jpokorny+rpm-wlroots@fedoraproject.org> - 0.5.0-1
- Updated to version 0.5.0 (0.2, 0.3, 0.4, 0.4.1 releases effectively skipped)
- Avoid building some parts that are not shipped in binary form, anyway
- Minor spec cleanup (clarify the licensing comment, licensecheck's NTP ~ MIT,
  ldconfig_scriptlets no longer relevant, arch-specific tweak no longer needed)

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 27 2018 Jan Pokorný <jpokorny+rpm-wlroots@fedoraproject.org> - 0.1-4
- Fix Firefox crash around text selection/clipboard
  (https://github.com/swaywm/wlroots/pull/1380)

* Tue Nov 27 2018 Jan Pokorný <jpokorny+rpm-wlroots@fedoraproject.org> - 0.1-3
- Make Firefox run smoother (https://github.com/swaywm/wlroots/pull/1384)

* Wed Nov 07 2018 Jan Pokorný <jpokorny+rpm-wlroots@fedoraproject.org> - 0.1-2
- Fix incorrect "pkgconfig" version

* Wed Oct 31 2018 Jan Pokorný <jpokorny+rpm-wlroots@fedoraproject.org> - 0.1-1
- Updated to historically first official release
- Turned off implicit enablement of all 'auto' build features under Meson,
  since xcb-errors is not available at this time
- Added BR: libpng
- Expanding spec comment on source files not covered with MIT license

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-0.9.20180106git03faf17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.1-0.8.20180106git03faf17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 13 2018 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.7.20180106git03faf17
- Updated snapshot

* Wed Jan 03 2018 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.6.20180102git767df15
- Initial import (#1529352)

* Wed Jan 03 2018 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.5.20180102git767df15
- Updated snapshot

* Sun Dec 31 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.4.20171229git80ed4d4
- Add licensing clarification
- Add BR: gcc

* Sat Dec 30 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.3.20171229git80ed4d4
- Updated snapshot

* Wed Dec 27 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.2.20171227giteeb7cd8
- Optimize spec-file

* Wed Dec 27 2017 Björn Esser <besser82@fedoraproject.org> - 0.0.1-0.1.20171227giteeb7cd8
- Initial rpm release (#1529352)
