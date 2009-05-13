#
# TODO:
#	- OpenAIS support
#
Summary:	The scalable High-Availability cluster resource manager
Name:		pacemaker
Version:	1.0.3
Release:	0.1
License:	GPL v2+; LGPL v2.1+
Group:		Applications/System
Source0:	http://hg.clusterlabs.org/pacemaker/stable-1.0/archive/Pacemaker-%{version}.tar.bz2
# Source0-md5:	b377be64de0920773168bda3abf54319
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-liborder.patch
URL:		http://clusterlabs.org/wiki/Main_Page
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel
BuildRequires:	gnutls-devel
BuildRequires:	heartbeat-devel >= 2.99
BuildRequires:	libesmtp-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	swig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	heartbeat
Provides:	group(haclient)
Provides:	user(hacluster)
Conflicts:	heartbeat < 2.99.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacemaker makes use of your cluster infrastructure (either OpenAIS or
Heartbeat) to stop, start and monitor the health of the services (aka.
resources) you want the cluster to provide.

It can do this for clusters of practically any size and comes with a
powerful dependency model that allows the administrator to accurately
express the relationships (both ordering and location) between the
cluster resources.

Pacemaker was formely a part of Heartbeat.

%package libs
Summary:	Pacemaker libraries
Group:		Libraries

%description libs
Shared libraries for Pacemaker.

%package devel
Summary:	Header files for Pacemaker libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Pacemaker
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Pacemaker libraries.

%package static
Summary:	Static Pacemaker libraries
Summary(pl.UTF-8):	Statyczne biblioteki Pacemaker
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Pacemaker libraries.

%prep
%setup -qn Pacemaker-1-0-Pacemaker-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--with-heartbeat \
	--without-ais \
	--with-snmp \
	--with-esmtp \
	--disable-fatal-warnings

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_docdir}/packages

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 60 haclient
%useradd -u 17 -d /var/lib/heartbeat/cores/hacluster -c "Heartbeat User" -g haclient hacluster

%files
%defattr(644,root,root,755)
%doc doc/README* doc/*.html doc/*.txt doc/AUTHORS doc/Design
%{_datadir}/pacemaker
%{_libdir}/heartbeat/*
%attr(755,root,root) %{_sbindir}/cibadmin
%attr(755,root,root) %{_sbindir}/crm_attribute
%attr(755,root,root) %{_sbindir}/crm_diff
%attr(755,root,root) %{_sbindir}/crm_failcount
%attr(755,root,root) %{_sbindir}/crm_master
%attr(755,root,root) %{_sbindir}/crm_mon
%attr(755,root,root) %{_sbindir}/crm
%attr(755,root,root) %{_sbindir}/crm_resource
%attr(755,root,root) %{_sbindir}/crm_standby
%attr(755,root,root) %{_sbindir}/crm_verify
%attr(755,root,root) %{_sbindir}/crmadmin
%attr(755,root,root) %{_sbindir}/iso8601
%attr(755,root,root) %{_sbindir}/attrd_updater
%attr(755,root,root) %{_sbindir}/ptest
%attr(755,root,root) %{_sbindir}/crm_shadow
%attr(755,root,root) %{_sbindir}/cibpipe
%attr(755,root,root) %{_sbindir}/crm_node
%attr(755,root,root) %{_sbindir}/crm_uuid
%{_mandir}/man8/*.8*
%dir %attr(750,hacluster,haclient) %{_var}/lib/heartbeat/crm
%dir %attr(750,hacluster,haclient) %{_var}/lib/pengine
%dir %attr(750,hacluster,haclient) %{_var}/run/crm
%dir %{_libdir}/ocf
%dir %{_libdir}/ocf/resource.d
%{_libdir}/ocf/resource.d/pacemaker
#%{_libexecdir}/lcrso/pacemaker.lcrso

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/lib*.so.[0-9]

%files devel
%defattr(644,root,root,755)
%{_includedir}/pacemaker
%{_includedir}/heartbeat/fencing
%{_libdir}/*.so
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
