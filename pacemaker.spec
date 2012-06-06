%bcond_with	corosync	# by default use heartbeat
%bcond_without	heartbeat	# by default use heartbeat
Summary:	The scalable High-Availability cluster resource manager
Name:		pacemaker
# version 1.1 is on the pacemaker-1_1 branch
Version:	1.0.12
Release:	1
License:	GPL v2+; LGPL v2.1+
Group:		Applications/System
Source0:	https://github.com/ClusterLabs/pacemaker-1.0/tarball/Pacemaker-%{version}
# Source0-md5:	f8ff6475e68ef8ce765305c24dc1d2a5
Source1:	%{name}.tmpfiles
Patch0:		%{name}-ncurses.patch
Patch1:		%{name}-libs.patch
URL:		http://clusterlabs.org/wiki/Main_Page
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
%{?with_corosync:BuildRequires:	corosync-devel}
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel
BuildRequires:	gnutls-devel
%{?with_heartbeat:BuildRequires: heartbeat-devel >= 2.99}
BuildRequires:	libesmtp-devel
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	ncurses-devel
BuildRequires:	net-snmp-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	swig
BuildRequires:	pciutils-devel
BuildRequires:	cluster-glue-libs-devel
Requires:	%{name}-libs = %{version}-%{release}
%{?with_corosync:Requires:	corosync}
%{?with_heartbeat:Requires:	heartbeat}
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
%setup -qn ClusterLabs-pacemaker-1.0-066152e
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	%{?with_heartbeat:--with-heartbeat} \
	%{!?with_heartbeat:--without-heartbeat} \
	%{?with_corosync:--with-ais} \
	%{?without_corosync:--without-ais} \
	--with-snmp \
	--with-esmtp \
	--disable-fatal-warnings

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/lib/tmpfiles.d

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_docdir}/pacemaker
rm $RPM_BUILD_ROOT%{_libdir}/heartbeat/plugins/RAExec/*.{la,a}

install %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 60 haclient
%useradd -u 17 -d /var/lib/heartbeat/cores/hacluster -c "Heartbeat User" -g haclient hacluster

%files
%defattr(644,root,root,755)
%doc doc/README* doc/*.html doc/*.txt AUTHORS COPYING* doc/Pacemaker_Explained
%{_datadir}/pacemaker
%dir %{_libdir}/heartbeat/plugins/RAExec
%attr(755,root,root) %{_libdir}/heartbeat/plugins/RAExec/*.so
%dir %{_libdir}/heartbeat/stonithdtest
%if %{with corosync}
%dir %{_libdir}/lcrso
%{_libdir}/lcrso/pacemaker.lcrso
%endif
%attr(755,root,root) %{_libdir}/heartbeat/stonithdtest/apitest
%attr(755,root,root) %{_libdir}/heartbeat/atest
%attr(755,root,root) %{_libdir}/heartbeat/attrd
%attr(755,root,root) %{_libdir}/heartbeat/cib
%attr(755,root,root) %{_libdir}/heartbeat/cibmon
%attr(755,root,root) %{_libdir}/heartbeat/crmd
%attr(755,root,root) %{_libdir}/heartbeat/haresources2cib.py
%attr(755,root,root) %{_libdir}/heartbeat/hb2openais.sh
%attr(755,root,root) %{_libdir}/heartbeat/pengine
%attr(755,root,root) %{_libdir}/heartbeat/pingd
%attr(755,root,root) %{_libdir}/heartbeat/stonithd
%attr(755,root,root) %{_libdir}/heartbeat/crm_primitive.py
%attr(755,root,root)%{_libdir}/heartbeat/hb2openais-helper.py
%{_libdir}/heartbeat/*.py[co]
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
%{py_sitedir}/crm
%{py_sitedir}/cts
%{_datadir}/snmp/mibs
%{_mandir}/man8/*.8*
%dir %attr(750,hacluster,haclient) %{_var}/lib/heartbeat/crm
%dir %attr(750,hacluster,haclient) %{_var}/lib/pengine
%dir %attr(750,hacluster,haclient) %{_var}/run/crm
%dir %{_prefix}/lib/ocf/resource.d/pacemaker
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/ClusterMon
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/Dummy
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/HealthCPU
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/HealthSMART
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/Stateful
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/SysInfo
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/SystemHealth
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/controld
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/o2cb
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/ping
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/pingd
/usr/lib/tmpfiles.d/%{name}.conf

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
