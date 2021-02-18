%global ver 1.4.1
%global gittag v%{ver}
%global commit dbd9c2bc98ef0cec7801a049f4bf8d61f7be36d0

%global shortcommit          %(c=%{commit}; echo ${c:0:7})
%define build_timestamp      %(date +"%Y%m%d")
%define snap                 %{?commit:.%{build_timestamp}git%{shortcommit}}
%define archive_name         %{?commit}%{!?commit:%{?gittag}}

Name:       mako
Version:    %{ver}
Release:    1%{snap}%{?dist}
Summary:    A lightweight notification daemon for Wayland.

License:    MIT
URL:        https://github.com/emersion/mako
Source0:    %{url}/archive/%{archive_name}.tar.gz#/%{name}-%{version}%{?snap}.tar.gz

BuildRequires: gcc
BuildRequires: meson
BuildRequires: systemd-devel
BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel >= 1.14
BuildRequires: cairo-devel
BuildRequires: pango-devel
BuildRequires: scdoc
BuildRequires: pkgconfig(gdk-pixbuf-2.0)

%description
%{summary}

%prep
%setup -q -n %{name}-%{!?commit:%{ver}}%{?commit}


%build
%meson -Dsd-bus-provider=libsystemd
%meson_build


%install
%meson_install
#mv %{buildroot}/contrib/systemd/mako.service %{_userunitdir}/%{name}.service


%files
#doc
%license LICENSE
%{_bindir}/mako
%{_bindir}/makoctl
%{_mandir}/man1/mako.1.gz
%{_mandir}/man5/mako.5.gz
%{_mandir}/man1/makoctl.1.gz
#%{_userunitdir}/%{name}.service
%{_datarootdir}/dbus-1/services/fr.emersion.mako.service


%changelog
* Thu Nov 22 2018 Jerzy Drozdz <rpmbuilder@jdsieci.pl> - 1.1-1.1
- Added missing build requisite

* Thu Nov 22 2018 Jerzy Drozdz <rpmbuilder@jdsieci.pl> - 1.1-1
- Initial build

