#
%bcond_without	corosync	# build with corosync stack
%bcond_without	heartbeat	# build without heartbeat stack
Summary:	The scalable High-Availability cluster resource manager
Name:		pacemaker
Version:	1.1.9
Release:	1
License:	GPL v2+; LGPL v2.1+
Group:		Applications/System
Source0:	https://github.com/ClusterLabs/pacemaker/archive/Pacemaker-%{version}.tar.gz
# Source0-md5:	24f3a2bdbac63e640062c207eb838016
Source1:	%{name}.tmpfiles
Source2:	%{name}.init
Source3:	%{name}.service
Patch0:		%{name}-libs.patch
URL:		http://clusterlabs.org/wiki/Main_Page
BuildRequires:	asciidoc
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
%{?with_corosync:BuildRequires:	corosync-devel >= 2.0}
BuildRequires:	e2fsprogs-devel
BuildRequires:	glib2-devel
BuildRequires:	gnutls-devel
%{?with_heartbeat:BuildRequires: heartbeat-devel >= 3.0.5-6}
BuildRequires:	libesmtp-devel
BuildRequires:	libqb
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
Requires:	cluster-glue
Requires:	resource-agents
Requires:	%{name}-libs = %{version}-%{release}
Provides:	group(haclient)
Provides:	user(hacluster)
Suggests:	pacemaker-shell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbol in libpe_status.so.3.0.0: get_object_root
# not handled by -libs patch, as it is a circular dependency
%define skip_post_check_so libpe_status.so.*

%description
Pacemaker makes use of your cluster infrastructure (either 
Corosync/OpenAIS or Heartbeat) to stop, start and monitor the health
of the services (aka.  resources) you want the cluster to provide.

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

%package heartbeat
Summary:	Pacemaker for Heartbeat cluster
Group:		Applications/System
Requires:	heartbeat
Obsoletes:	%{name} < 1.1
Conflicts:	heartbeat < 2.99.0
Requires:	%{name} = %{version}-%{release}

%description heartbeat
This package allows using Pacemaker on a Heartbeat cluster.

%package corosync
Summary:	Pacemaker for Corosync cluster
Group:		Applications/System
Requires:	corosync
Requires:	%{name} = %{version}-%{release}

%description corosync
This package allows using Pacemaker on a Corosync cluster.

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
%setup -qn pacemaker-Pacemaker-%{version}
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	CPPFLAGS="%{rpmcppflags} %{?with_heartbeat:-I/usr/include/heartbeat}" \
	--with-heartbeat%{!?with_heartbeat:=no} \
	--with-corosync%{!?with_corosync:=no} \
	--with-snmp \
	--with-esmtp \
	--with-acl \
	--with-initdir=/etc/rc.d/init.d \
	--disable-fatal-warnings

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/usr/lib/tmpfiles.d,/etc/rc.d/init.d,%{systemdunitdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -r $RPM_BUILD_ROOT%{_docdir}/pacemaker

install %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 60 haclient
%useradd -u 17 -d /var/lib/heartbeat/cores/hacluster -c "Heartbeat User" -g haclient hacluster

%post corosync
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%systemd_post %{name}.service

%preun
if [ "$1" = "0" ]; then
        %service %{name} stop
        /sbin/chkconfig --del %{name}
fi
%systemd_preun %{name}.service

%postun corosync
%systemd_reload

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/README* doc/*.html doc/*.txt AUTHORS COPYING*
%{_datadir}/pacemaker
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/attrd
%attr(755,root,root) %{_libdir}/%{name}/cib
%attr(755,root,root) %{_libdir}/%{name}/cibmon
%attr(755,root,root) %{_libdir}/%{name}/crmd
%attr(755,root,root) %{_libdir}/%{name}/lrmd
%attr(755,root,root) %{_libdir}/%{name}/lrmd_test
%attr(755,root,root) %{_libdir}/%{name}/pengine
%attr(755,root,root) %{_libdir}/%{name}/stonith-test
%attr(755,root,root) %{_libdir}/%{name}/stonithd
%attr(755,root,root) %{_bindir}/ccs2cib
%attr(755,root,root) %{_bindir}/ccs_flatten
%attr(755,root,root) %{_bindir}/disable_rgmanager
%attr(755,root,root) %{_sbindir}/attrd_updater
%attr(755,root,root) %{_sbindir}/cibadmin
%attr(755,root,root) %{_sbindir}/crm_attribute
%attr(755,root,root) %{_sbindir}/crm_diff
%attr(755,root,root) %{_sbindir}/crm_error
%attr(755,root,root) %{_sbindir}/crm_failcount
%attr(755,root,root) %{_sbindir}/crm_master
%attr(755,root,root) %{_sbindir}/crm_mon
%attr(755,root,root) %{_sbindir}/crm_node
%attr(755,root,root) %{_sbindir}/crm_report
%attr(755,root,root) %{_sbindir}/crm_resource
%attr(755,root,root) %{_sbindir}/crm_simulate
%attr(755,root,root) %{_sbindir}/crm_shadow
%attr(755,root,root) %{_sbindir}/crm_standby
%attr(755,root,root) %{_sbindir}/crm_ticket
%attr(755,root,root) %{_sbindir}/crm_uuid
%attr(755,root,root) %{_sbindir}/crm_verify
%attr(755,root,root) %{_sbindir}/crmadmin
%attr(755,root,root) %{_sbindir}/fence_legacy
%attr(755,root,root) %{_sbindir}/fence_pcmk
%attr(755,root,root) %{_sbindir}/iso8601
%attr(755,root,root) %{_sbindir}/stonith_admin
%{py_sitedir}/cts
%{_datadir}/snmp/mibs
%{_mandir}/man8/*.8*
%{_mandir}/man7/*.7*
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
%dir /var/lib/%{name}
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/blackbox
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/cib
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/pengine

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/lib*.so.[0-9]

%if %{with heartbeat}
%files heartbeat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/heartbeat/attrd
%attr(755,root,root) %{_libdir}/heartbeat/cib
%attr(755,root,root) %{_libdir}/heartbeat/crmd
%attr(755,root,root) %{_libdir}/heartbeat/pengine
%attr(755,root,root) %{_libdir}/heartbeat/stonithd
%endif

%if %{with corosync}
%files corosync
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pacemakerd
%attr(755,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/%{name}.service
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/pacemaker
%{_libdir}/*.so
%{_libdir}/*.la
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/*.a
