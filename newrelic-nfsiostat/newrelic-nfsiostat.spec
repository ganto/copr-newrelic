%global debug_package %{nil}

Name:       newrelic-nfsiostat
Version:    0.2.5
Release:    2%{?dist}
Summary:    NFSIOSTAT plugin for New Relic

Group:      Applications/System
License:    GPLv2
URL:        https://github.com/LarkIT/newrelic-nfsiostat
Source0:    https://github.com/LarkIT/newrelic-nfsiostat/archive/%{name}-v%{version}.tar.gz
Source1:    newrelic-nfsiostat.service
Patch0:     newrelic-nfsiostat-0.2.5-Fix-NFSv4-support-by-fixing-check-for-readdirplus.patch
Patch1:     newrelic-nfsiostat-0.2.5-Remove-sysvinit-support.patch
Patch2:     newrelic-nfsiostat-0.2.5-Dont-install-doc.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  systemd

Requires:       python2
%if 0%{?rhel} == 7
Requires:       python-daemon
%else
Requires:       python2-daemon
%endif
Requires:       python2-psutil
%{?systemd_requires}

%description
A New Relic plugin to send statistics from nfsiostat to NewRelic.

%prep
%setup -q -n %{name}-%{name}-v%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%py2_build

%install
%py2_install
install -d -m 0755 %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_preun %{name}.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license doc/LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/newrelic-nfsiostat.conf
%{_bindir}/newrelic-nfsiostat
%{_unitdir}/%{name}.service
%{python2_sitelib}/*

%changelog
* Sun Jan 20 2019 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.2.5-2
- Rework for CentOS 7 and Fedora
- Include patch for NFSv4 fix

* Mon Nov 24 2014 Tommy McNeely <tommy@lark-it.com> 0.2.5-1
- fixes #16 - More complete fix to the /dev/tty issues (See Issue #7)

* Tue Nov 04 2014 Tommy McNeely <tommy@lark-it.com> 0.2.4-1
- Fixed Issue #13 - Crash on error handling (See Issue #8)

* Tue Nov 04 2014 Tommy McNeely <tommy@lark-it.com> 0.2.3-1
- Updating to v0.2.3
- Fixed Issue #8 - Crash on httplib.BadStatusLine
- Fixed Issue #7 - Crash on start at boot (No such device /dev/tty)
- Fixed Issue #6 - Fix for no data when using NFSv4 (ReadDirPlus)

* Thu Jun 26 2014 Tommy McNeely <tommy@lark-it.com> 0.2.2-1
- Updating to v0.2.2
- Adds NFS Aggregate Stats

* Thu Jun 26 2014 Tommy McNeely <tommy@lark-it.com> 0.2.1-1
- Fixing scripts, package names, etc

* Thu Jun 26 2014 Tommy McNeely <tommy@lark-it.com> 0.2.0-1
- Initial RPM after forking from NewRHELic
