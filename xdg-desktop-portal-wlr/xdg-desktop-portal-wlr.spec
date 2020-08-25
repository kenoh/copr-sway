%global ver 0.1.0
%global gittag v%{ver}
%global commit 61db8968f999a23fc7b604fcf7a82a83e7cf268e

%global shortcommit          %(c=%{commit}; echo ${c:0:7})
%define build_timestamp      %(date +"%Y%m%d")
%define snap                 %{?commit:.%{build_timestamp}git%{shortcommit}}
%define archive_name         %{?commit}%{!?commit:%{?gittag}}

Name:       xdg-desktop-portal-wlr
Version:    %{ver}
Release:    1%{snap}%{?dist}
Summary:    xdg-desktop-portal backend for wlroots 

License:    MIT
URL:        https://github.com/emersion/xdg-desktop-portal-wlr
Source0:    %{url}/archive/%{archive_name}.tar.gz#/%{name}-%{version}%{?snap}.tar.gz

BuildRequires: gcc
BuildRequires: meson
BuildRequires: pkgconfig(libsystemd)
BuildRequires: wayland-devel
BuildRequires: wayland-protocols-devel >= 1.14
BuildRequires: pkgconfig(libpipewire-0.3)

%description
%{summary}

%prep
%setup -q -n %{name}-%{!?commit:%{ver}}%{?commit}


%build
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%{_libexecdir}/%{name}
%{_userunitdir}/%{name}.service
%{_datarootdir}/dbus-1/services/org.freedesktop.impl.portal.desktop.wlr.service
%{_datarootdir}/xdg-desktop-portal/portals/wlr.portal


%changelog
