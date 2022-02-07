#
# Conditional build:
%bcond_without	corosync	# Corosync stack support
%bcond_without	servicelog	# ServiceLog support [IBM PPC specific]
%bcond_without	ipmi		# IPMI ServiceLog support [IBM PPC specific]
%bcond_without	doc		# documentation
%bcond_without	static_libs	# static libraries
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
Version:	2.0.5
Release:	1
License:	GPL v2+, LGPL v2.1+
Group:		Applications/System
#Source0Download: https://github.com/ClusterLabs/pacemaker/releases
Source0:	https://github.com/ClusterLabs/pacemaker/archive/Pacemaker-%{version}.tar.gz
# Source0-md5:	c36c8ed401e39ff3e727ba4bf5fcc2e7
Source1:	%{name}.tmpfiles
Source2:	%{name}.init
Source3:	%{name}.service
Patch1:		%{name}-manpage_xslt.patch
Patch2:		%{name}-update.patch
URL:		https://wiki.clusterlabs.org/wiki/Pacemaker
%{?with_ipmi:BuildRequires:	OpenIPMI-devel}
BuildRequires:	asciidoc
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.11
BuildRequires:	bzip2-devel
BuildRequires:	cluster-glue-libs-devel
%{?with_corosync:BuildRequires:	corosync-devel >= 2.0}
BuildRequires:	dbus-devel
BuildRequires:	docbook-style-xsl
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.16.0
BuildRequires:	gnutls-devel >= 2.12.0
BuildRequires:	help2man
BuildRequires:	libltdl-devel
BuildRequires:	libqb-devel >= 0.17.0
%{?with_servicelog:BuildRequires:	libservicelog-devel}
BuildRequires:	libtool >= 2:2
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	libxslt-devel
BuildRequires:	libxslt-progs
BuildRequires:	ncurses-devel >= 5.4
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	systemd-units
%if %{with doc}
BuildRequires:	inkscape >= 1.0
BuildRequires:	publican
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	cluster-glue
Requires:	resource-agents
Suggests:	pacemaker-shell
Provides:	group(haclient)
Provides:	user(hacluster)
Obsoletes:	pacemaker-heartbeat < 2.0
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
Requires:	glib2 >= 1:2.16.0
Requires:	gnutls-libs >= 2.12.0
Requires:	libqb >= 0.17.0

%description libs
Shared libraries for Pacemaker.

%description libs -l pl.UTF-8
Biblioteki współdzielone Pacemakera.

%package devel
Summary:	Header files for Pacemaker libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek Pacemakera
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bzip2-devel
Requires:	dbus-devel
Requires:	glib2-devel >= 1:2.16.0
Requires:	gnutls-devel >= 2.12.0
Requires:	libqb-devel >= 0.17.0
Requires:	libxml2-devel >= 2.0
Requires:	libxslt-devel
Requires:	libuuid-devel
Requires:	ncurses-devel

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

%package corosync
Summary:	Pacemaker for Corosync cluster
Summary(pl.UTF-8):	Pacemaker dla klastra Corosync
Group:		Applications/System
Requires:	%{name} = %{version}-%{release}
Requires:	corosync >= 2.0
Requires:	systemd-units >= 38

%description corosync
This package allows using Pacemaker on a Corosync cluster.

%description corosync -l pl.UTF-8
Ten pakiet pozwala na używanie Pacemakera na klastrze Corosync.

%package doc
Summary:	Pacemaker documentation
Summary(pl.UTF-8):	Dokumentacja do Pacemakera
Group:		Documentation
BuildArch:	noarch

%description doc
Pacemaker documentation.

%description doc -l pl.UTF-8
Dokumentacja do Pacemakera.

%prep
%setup -qn pacemaker-Pacemaker-%{version}
%patch1 -p1
%patch2 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}

# enable systemd explicitly to avoid configure checks via dbus-send or systemctl
%configure \
	PYTHON=%{__python} \
	--disable-fatal-warnings \
	--disable-silent-rules \
	%{__enable_disable static_libs static} \
	--enable-systemd \
	--disable-upstart \
	--with-acl \
	--with-corosync%{!?with_corosync:=no} \
	--with-initdir=/etc/rc.d/init.d

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/run/crm,/var/log}

%{__make} install \
	mibdir=%{_datadir}/mibs \
	DESTDIR=$RPM_BUILD_ROOT

touch $RPM_BUILD_ROOT/var/log/pacemaker.log

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/pacemaker/tests
# package as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/pacemaker/{COPYING,README.markdown,crm_fencing.*,licenses}

install -D %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf
%if %{with corosync}
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install -D %{SOURCE3} $RPM_BUILD_ROOT%{systemdunitdir}/%{name}.service
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 60 haclient
%useradd -u 17 -d /var/lib/pacemaker/cores -c "Heartbeat User" -g haclient hacluster

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
%doc ChangeLog README.markdown doc/*.html doc/security.txt doc/{openstack,pcs-crmsh-quick-ref}.md
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
%attr(755,root,root) %{_sbindir}/crm_rule
%attr(755,root,root) %{_sbindir}/crm_simulate
%attr(755,root,root) %{_sbindir}/crm_shadow
%attr(755,root,root) %{_sbindir}/crm_standby
%attr(755,root,root) %{_sbindir}/crm_ticket
%attr(755,root,root) %{_sbindir}/crm_verify
%attr(755,root,root) %{_sbindir}/crmadmin
%attr(755,root,root) %{_sbindir}/fence_legacy
%attr(755,root,root) %{_sbindir}/iso8601
%attr(755,root,root) %{_sbindir}/stonith_admin
%if %{with servicelog}
%if %{with ipmi}
%attr(755,root,root) %{_sbindir}/ipmiservicelogd
%endif
%attr(755,root,root) %{_sbindir}/notifyServicelogEvent
%endif
%dir %{_libexecdir}/%{name}
%attr(755,root,root) %{_libexecdir}/%{name}/attrd
%attr(755,root,root) %{_libexecdir}/%{name}/cib
%attr(755,root,root) %{_libexecdir}/%{name}/cibmon
%attr(755,root,root) %{_libexecdir}/%{name}/crmd
%attr(755,root,root) %{_libexecdir}/%{name}/cts-exec-helper
%attr(755,root,root) %{_libexecdir}/%{name}/cts-fence-helper
%attr(755,root,root) %{_libexecdir}/%{name}/cts-log-watcher
%attr(755,root,root) %{_libexecdir}/%{name}/cts-support
%attr(755,root,root) %{_libexecdir}/%{name}/lrmd
%attr(755,root,root) %{_libexecdir}/%{name}/pacemaker-attrd
%attr(755,root,root) %{_libexecdir}/%{name}/pacemaker-based
%attr(755,root,root) %{_libexecdir}/%{name}/pacemaker-controld
%attr(755,root,root) %{_libexecdir}/%{name}/pacemaker-execd
%attr(755,root,root) %{_libexecdir}/%{name}/pacemaker-fenced
%attr(755,root,root) %{_libexecdir}/%{name}/pacemaker-schedulerd
%attr(755,root,root) %{_libexecdir}/%{name}/pengine
%attr(755,root,root) %{_libexecdir}/%{name}/stonithd
%{_datadir}/pacemaker
%{_datadir}/mibs/PCMK-MIB.txt
%{py_sitescriptdir}/cts
%{systemdunitdir}/crm_mon.service
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/pacemaker
%attr(750,root,haclient) %dir %{_sysconfdir}/pacemaker
%ghost /var/log/pacemaker.log
%{_mandir}/man7/ocf_pacemaker_*.7*
%{_mandir}/man7/pacemaker-controld.7*
%{_mandir}/man7/pacemaker-fenced.7*
%{_mandir}/man7/pacemaker-schedulerd.7*
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
%{_mandir}/man8/crm_rule.8*
%{_mandir}/man8/crm_shadow.8*
%{_mandir}/man8/crm_simulate.8*
%{_mandir}/man8/crm_standby.8*
%{_mandir}/man8/crm_ticket.8*
%{_mandir}/man8/crm_verify.8*
%{_mandir}/man8/crmadmin.8*
%{_mandir}/man8/fence_legacy.8*
%{_mandir}/man8/iso8601.8*
%{_mandir}/man8/stonith_admin.8*
%if %{with servicelog}
%if %{with ipmi}
%{_mandir}/man8/ipmiservicelogd.8*
%endif
%{_mandir}/man8/notifyServicelogEvent.8*
%endif

%dir %{_prefix}/lib/ocf/resource.d/pacemaker
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/ClusterMon
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/Dummy
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/HealthCPU
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/HealthIOWait
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/HealthSMART
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/Stateful
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/SysInfo
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/SystemHealth
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/attribute
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/controld
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/ifspeed
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/o2cb
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/ping
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/pingd
%attr(755,root,root) %{_prefix}/lib/ocf/resource.d/pacemaker/remote

%dir /var/lib/%{name}
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/blackbox
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/cib
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/cores
%dir %attr(750,hacluster,haclient) /var/lib/%{name}/pengine
%dir %attr(770,hacluster,haclient) /var/log/%{name}
%dir %attr(770,hacluster,haclient) /var/log/%{name}/bundles
%dir %attr(750,hacluster,haclient) %{_var}/run/crm
%{systemdtmpfilesdir}/%{name}.conf

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcib.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcib.so.27
%attr(755,root,root) %{_libdir}/libcrmcluster.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrmcluster.so.29
%attr(755,root,root) %{_libdir}/libcrmcommon.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrmcommon.so.34
%attr(755,root,root) %{_libdir}/libcrmservice.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcrmservice.so.28
%attr(755,root,root) %{_libdir}/liblrmd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblrmd.so.28
%attr(755,root,root) %{_libdir}/libpacemaker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpacemaker.so.1
%attr(755,root,root) %{_libdir}/libpe_rules.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpe_rules.so.26
%attr(755,root,root) %{_libdir}/libpe_status.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpe_status.so.28
%attr(755,root,root) %{_libdir}/libstonithd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstonithd.so.26

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcib.so
%attr(755,root,root) %{_libdir}/libcrmcluster.so
%attr(755,root,root) %{_libdir}/libcrmcommon.so
%attr(755,root,root) %{_libdir}/libcrmservice.so
%attr(755,root,root) %{_libdir}/liblrmd.so
%attr(755,root,root) %{_libdir}/libpacemaker.so
%attr(755,root,root) %{_libdir}/libpe_rules.so
%attr(755,root,root) %{_libdir}/libpe_status.so
%attr(755,root,root) %{_libdir}/libstonithd.so
%{_libdir}/libcib.la
%{_libdir}/libcrmcluster.la
%{_libdir}/libcrmcommon.la
%{_libdir}/libcrmservice.la
%{_libdir}/liblrmd.la
%{_libdir}/libpacemaker.la
%{_libdir}/libpe_rules.la
%{_libdir}/libpe_status.la
%{_libdir}/libstonithd.la
%{_includedir}/pacemaker
%{_pkgconfigdir}/libpacemaker.pc
%{_pkgconfigdir}/pacemaker.pc
%{_pkgconfigdir}/pacemaker-cib.pc
%{_pkgconfigdir}/pacemaker-cluster.pc
%{_pkgconfigdir}/pacemaker-fencing.pc
%{_pkgconfigdir}/pacemaker-lrmd.pc
%{_pkgconfigdir}/pacemaker-pe_rules.pc
%{_pkgconfigdir}/pacemaker-pe_status.pc
%{_pkgconfigdir}/pacemaker-service.pc
%{_npkgconfigdir}/pacemaker-schemas.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libcib.a
%{_libdir}/libcrmcluster.a
%{_libdir}/libcrmcommon.a
%{_libdir}/libcrmservice.a
%{_libdir}/liblrmd.a
%{_libdir}/libpacemaker.a
%{_libdir}/libpe_rules.a
%{_libdir}/libpe_status.a
%{_libdir}/libstonithd.a
%endif

%files remote
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pacemaker-remoted
%attr(755,root,root) %{_sbindir}/pacemaker_remoted
%attr(755,root,root) /etc/rc.d/init.d/pacemaker_remote
%{systemdunitdir}/pacemaker_remote.service
%{_mandir}/man8/pacemaker-remoted.8*

%if %{with corosync}
%files corosync
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pacemakerd
%attr(755,root,root) /etc/rc.d/init.d/%{name}
%{systemdunitdir}/%{name}.service
%{_mandir}/man8/pacemakerd.8*
%endif

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%dir %{_docdir}/pacemaker
%{_docdir}/pacemaker/Clusters_from_Scratch
%{_docdir}/pacemaker/Pacemaker_Administration
%{_docdir}/pacemaker/Pacemaker_Development
%{_docdir}/pacemaker/Pacemaker_Explained
%{_docdir}/pacemaker/Pacemaker_Remote
%endif
