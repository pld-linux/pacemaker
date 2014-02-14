#
# Conditional build:
%bcond_without	corosync	# Corosync stack support
%bcond_without	heartbeat	# Heartbeat stack support
%bcond_without	servicelog	# ServiceLog support [IBM PPC specific]
%bcond_without	ipmi		# IPMI ServiceLog support [IBM PPC specific]
#
%ifnarch ppc ppc64
%undefine	with_servicelog
%endif
%if %{without servicelog}
%undefine	with_ipmi
%endif
Summary:	The scalable High-Availability cluster resource manager
Summary(pl.UTF-8):	Skalowalny zarządca zasobów klastrów o wysokiej dostępności
Name:		pacemaker
Version:	1.1.11
Release:	1
License:	GPL v2+, LGPL v2.1+
Group:		Applications/System
Source0:	https://github.com/ClusterLabs/pacemaker/archive/Pacemaker-%{version}.tar.gz
# Source0-md5:	7cbe4f8ef2b300c3426a0c12a0c67c93
Source1:	%{name}.tmpfiles
Source2:	%{name}.init
Source3:	%{name}.service
Patch0:		%{name}-automake.patch
Patch1:		%{name}-manpage_xslt.patch
Patch2:		%{name}-update.patch
Patch3:		%{name}-man.patch
Patch4:		%{name}-libs.patch
URL:		http://clusterlabs.org/wiki/Main_Page
%{?with_ipmi:BuildRequires:	OpenIPMI-devel}
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	cluster-glue-libs-devel
%{?with_corosync:BuildRequires:	corosync-devel >= 2.0}
BuildRequires:	dbus-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	e2fsprogs-devel
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	gnutls-devel
BuildRequires:	help2man
%{?with_heartbeat:BuildRequires:	heartbeat-devel >= 3.0.5-6}
BuildRequires:	libesmtp-devel
BuildRequires:	libltdl-devel
BuildRequires:	libqb-devel >= 0.13
%{?with_servicelog:BuildRequires:	libservicelog-devel}
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel >= 5.4
BuildRequires:	net-snmp-devel
BuildRequires:	pam-devel
BuildRequires:	pciutils-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	systemd-units
BuildRequires:	swig
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cluster-glue
Requires:	resource-agents
Provides:	group(haclient)
Provides:	user(hacluster)
Suggests:	pacemaker-shell
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Pacemaker makes use of your cluster infrastructure (either 
Corosync/OpenAIS or Heartbeat) to stop, start and monitor the health
of the services (aka. resources) you want the cluster to provide.

It can do this for clusters of practically any size and comes with a
powerful dependency model that allows the administrator to accurately
express the relationships (both ordering and location) between the
cluster resources.

Pacemaker was formely a part of Heartbeat.

%description -l pl.UTF-8
Pacemaker wykorzystuje infrastrukturę klastrową (Corosync/OpenAIS lub
Heartbeat) do zatrzymywania, uruchamiania i monitorowania działania
usług (tzw. zasobów), które ma udostępniać klaster.

Jest w stanie obsłużyć klastry praktycznie dowolnych rozmiarów,
zawiera elastyczny model zależności, pozwalający administratorowi
dokładnie opisać powiązania (zarówno kolejność, jak i położenie)
między zasobami klastra.

Pacemaker był wcześniej częścią pakietu Heartbeat.

%package libs
Summary:	Pacemaker libraries
Summary(pl.UTF-8):	Biblioteki Pacemakera
Group:		Libraries

%description libs
Shared libraries for Pacemaker.

%description libs -l pl.UTF-8
Biblioteki współdzielone Pacemakera.

%package devel
Summary:	Header files for Pacemaker libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Pacemakera
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Pacemaker libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Pacemakera.

%package static
Summary:	Static Pacemaker libraries
Summary(pl.UTF-8):	Statyczne biblioteki Pacemakera
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Pacemaker libraries.

%description static -l pl.UTF-8
Statyczne biblioteki Pacemakera.

%package heartbeat
Summary:	Pacemaker for Heartbeat cluster
Summary(pl.UTF-8):	Pacemaker dla klastra Heartbeat
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	heartbeat
Obsoletes:	pacemaker < 1.1
Conflicts:	heartbeat < 2.99.0

%description heartbeat
This package allows using Pacemaker on a Heartbeat cluster.

%description heartbeat -l pl.UTF-8
Ten pakiet pozwala na używanie Pacemakera na klastrze Heartbeat.

%package corosync
Summary:	Pacemaker for Corosync cluster
Summary(pl.UTF-8):	Pacemaker dla klastra Corosync
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	corosync
Requires:	systemd-units >= 38
%{?with_heartbeat:%requires_eq	heartbeat-libs}

%description corosync
This package allows using Pacemaker on a Corosync cluster.

%description corosync -l pl.UTF-8
Ten pakiet pozwala na używanie Pacemakera na klastrze Corosync.

%package remote
Summary:	Remote services manager for Pacemaker
Summary(pl.UTF-8):	Zarządca usług zdalnych dla Pacemakera
Group:		Applications/System
Requires:	systemd-units >= 38
Requires:	%{name} = %{version}-%{release}

%description remote
This package allows running Pacemaker-managed services on 'virtual'
nodes without actual cluster stack. This is useful to manage services
in virtual machines or containers running on a Pacemaker cluster.

%description remote -l pl.UTF-8
Ten pakiet pozwala na uruchamianie usług zarządzanych przez Pacemakera
na węzłach "wirtualnych" bez zainstalowanego całego stosu klastrowego.
Jest to przydatne przy zarządzaniu usługami na maszynach wirtualncych
lub w kontenerach uruchomionych na klastrze opartym o Pacemaker.

%prep
%setup -qn pacemaker-Pacemaker-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

CPPFLAGS="%{rpmcppflags} %{?with_heartbeat:-I/usr/include/heartbeat}"
%configure \
	--with-acl \
	--with-corosync%{!?with_corosync:=no} \
	--with-esmtp \
	--with-heartbeat%{!?with_heartbeat:=no} \
	--with-initdir=/etc/rc.d/init.d \
	--with-snmp \
	--disable-fatal-warnings \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/pacemaker

install -D %{SOURCE1} $RPM_BUILD_ROOT/usr/lib/tmpfiles.d/%{name}.conf
%if %{with corosync}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
%endif

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

%preun corosync
%systemd_preun %{name}.service

%postun corosync
%systemd_reload

%post remote
/sbin/chkconfig --add pacemaker_remote
%service pacemaker_remote restart "pacemaker_remote daemon"
%systemd_post pacemaker_remote.service

%preun remote
%systemd_preun %{name}.service

%postun remote
%systemd_reload

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/README* doc/*.html doc/*.txt AUTHORS COPYING*
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
%attr(755,root,root) %{_sbindir}/crm_verify
%attr(755,root,root) %{_sbindir}/crmadmin
%attr(755,root,root) %{_sbindir}/fence_legacy
%attr(755,root,root) %{_sbindir}/fence_pcmk
%attr(755,root,root) %{_sbindir}/iso8601
%attr(755,root,root) %{_sbindir}/stonith_admin
%if %{with servicelog}
%if %{with ipmi}
%attr(755,root,root) %{_sbindir}/ipmiservicelogd
%endif
%attr(755,root,root) %{_sbindir}/notifyServicelogEvent
%endif
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
%{_datadir}/pacemaker
%{_datadir}/snmp/mibs/PCMK-MIB.txt
%{py_sitedir}/cts
%{_mandir}/man7/crmd.7*
%{_mandir}/man7/ocf_pacemaker_*.7*
%{_mandir}/man7/pengine.7*
%{_mandir}/man7/stonithd.7*
%{_mandir}/man8/attrd_updater.8*
%{_mandir}/man8/cibadmin.8*
%{_mandir}/man8/crm_attribute.8*
%{_mandir}/man8/crm_diff.8*
%{_mandir}/man8/crm_error.8*
%{_mandir}/man8/crm_failcount.8*
%{_mandir}/man8/crm_master.8*
%{_mandir}/man8/crm_mon.8*
%{_mandir}/man8/crm_node.8*
%{_mandir}/man8/crm_report.8*
%{_mandir}/man8/crm_resource.8*
%{_mandir}/man8/crm_shadow.8*
%{_mandir}/man8/crm_simulate.8*
%{_mandir}/man8/crm_standby.8*
%{_mandir}/man8/crm_ticket.8*
%{_mandir}/man8/crm_verify.8*
%{_mandir}/man8/crmadmin.8*
%{_mandir}/man8/fence_legacy.8*
%{_mandir}/man8/fence_pcmk.8*
%{_mandir}/man8/iso8601.8*
%{_mandir}/man8/stonith_admin.8*
%if %{with servicelog}
%{_mandir}/man8/notifyServicelogEvent.8*
%endif

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
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/remote

%dir /var/lib/%{name}
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/blackbox
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/cib
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/pengine
%dir %attr(750,hacluster,haclient) %{_var}/run/crm
/usr/lib/tmpfiles.d/%{name}.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcib.so.3
%attr(755,root,root) %{_libdir}/libcrmcluster.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrmcluster.so.4
%attr(755,root,root) %{_libdir}/libcrmcommon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrmcommon.so.3
%attr(755,root,root) %{_libdir}/libcrmservice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrmservice.so.1
%attr(755,root,root) %{_libdir}/liblrmd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblrmd.so.1
%attr(755,root,root) %{_libdir}/libpe_rules.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpe_rules.so.2
%attr(755,root,root) %{_libdir}/libpe_status.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpe_status.so.4
%attr(755,root,root) %{_libdir}/libpengine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpengine.so.4
%attr(755,root,root) %{_libdir}/libstonithd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstonithd.so.2
%attr(755,root,root) %{_libdir}/libtransitioner.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtransitioner.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcib.so
%attr(755,root,root) %{_libdir}/libcrmcluster.so
%attr(755,root,root) %{_libdir}/libcrmcommon.so
%attr(755,root,root) %{_libdir}/libcrmservice.so
%attr(755,root,root) %{_libdir}/liblrmd.so
%attr(755,root,root) %{_libdir}/libpe_rules.so
%attr(755,root,root) %{_libdir}/libpe_status.so
%attr(755,root,root) %{_libdir}/libpengine.so
%attr(755,root,root) %{_libdir}/libstonithd.so
%attr(755,root,root) %{_libdir}/libtransitioner.so
%{_libdir}/libcib.la
%{_libdir}/libcrmcluster.la
%{_libdir}/libcrmcommon.la
%{_libdir}/libcrmservice.la
%{_libdir}/liblrmd.la
%{_libdir}/libpe_rules.la
%{_libdir}/libpe_status.la
%{_libdir}/libpengine.la
%{_libdir}/libstonithd.la
%{_libdir}/libtransitioner.la
%{_includedir}/pacemaker
%{_pkgconfigdir}/pacemaker.pc
%{_pkgconfigdir}/pacemaker-cib.pc
%{_pkgconfigdir}/pacemaker-cluster.pc
%{_pkgconfigdir}/pacemaker-fencing.pc
%{_pkgconfigdir}/pacemaker-lrmd.pc
%{_pkgconfigdir}/pacemaker-pengine.pc
%{_pkgconfigdir}/pacemaker-service.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libcib.a
%{_libdir}/libcrmcluster.a
%{_libdir}/libcrmcommon.a
%{_libdir}/libcrmservice.a
%{_libdir}/liblrmd.a
%{_libdir}/libpe_rules.a
%{_libdir}/libpe_status.a
%{_libdir}/libpengine.a
%{_libdir}/libstonithd.a
%{_libdir}/libtransitioner.a

%files remote
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pacemaker_remoted
%attr(755,root,root) /etc/rc.d/init.d/pacemaker_remote
%{systemdunitdir}/pacemaker_remote.service
%{_mandir}/man8/pacemaker_remoted.8*

%if %{with heartbeat}
%files heartbeat
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/crm_uuid
%attr(755,root,root) %{_libdir}/heartbeat/attrd
%attr(755,root,root) %{_libdir}/heartbeat/cib
%attr(755,root,root) %{_libdir}/heartbeat/crmd
%attr(755,root,root) %{_libdir}/heartbeat/pengine
%attr(755,root,root) %{_libdir}/heartbeat/stonithd
%{_mandir}/man8/crm_uuid.8*
%endif

%if %{with corosync}
%files corosync
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pacemakerd
%attr(755,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/%{name}.service
%{_mandir}/man8/pacemakerd.8*
%endif
