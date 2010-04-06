%include	/usr/lib/rpm/macros.java
Summary:	JA-SIG Central Authentication Service
Name:		cas
Version:	3.4.2
Release:	1
License:	MIT License
Group:		Networking/Daemons/Java/Servlets
Source0:	http://www.ja-sig.org/downloads/cas/%{name}-server-%{version}-release.tar.gz
# Source0-md5:	3a7dfd70be008053b8619509dcc45be9
Source1:	%{name}-context.xml
URL:		http://www.ja-sig.org/products/cas/
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.546
Requires:	jpackage-utils
Requires:	tomcat >= 6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define webappdir %{_datadir}/%{name}
%define libdir    %{_datadir}/%{name}/WEB-INF/lib
%define	logdir    %{_var}/log/%{name}

%description
CAS is an authentication system originally created by Yale University
to provide a trusted way for an application to authenticate a user.
CAS became a JA-SIG project in December 2004.

CAS provides enterprise single sign on service. It features:

- An open and well-documented protocol
- An open-source Java server component
- A library of clients for Java, .Net, PHP, Perl, Apache, uPortal and
  others
- Integrates with uPortal, BlueSocket, TikiWiki, Mule, Liferay, Moodle
  and others
- Community documentation and implementation support
- An extensive community of adopters

%package authenticator-spnego
Summary:	Spnego authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-spnego
Spnego authentication backend for CAS Server.

%package authenticator-x509
Summary:	x509 authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-x509
X509 client certificates authentication backend for CAS Server.

%package authenticator-openid
Summary:	OpenID authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-openid
OpenID authentication backend for CAS Server.

%package authenticator-legacy
Summary:	Legacy authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-legacy
Legacy authentication backend for CAS Server.

%package authenticator-radius
Summary:	Radius authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-radius
Radius authentication backend for CAS Server.

%package authenticator-ldap
Summary:	LDAP authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-ldap
LDAP authentication backend for CAS Server.

%package authenticator-generic
Summary:	Generic authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-generic
Generic authentication backend for CAS Server.

%package authenticator-trusted
Summary:	Trusted authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-trusted
Trusted authentication backend for CAS Server.

%package authenticator-jdbc
Summary:	JDBC authenticator for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description authenticator-jdbc
JDBC authentication backend for CAS Server.

%package integration-berkeleydb
Summary:	Berkeleydb ticket registry for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description integration-berkeleydb
BerkeleyDB integration for CAS Server allows to store ticket registry
in berkeleyDB.

%package integration-jboss
Summary:	Jboss ticket registry for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description integration-jboss
Jboss integration for CAS Server allows to store ticket registry in
Jboss internal authentication system.

%package integration-memcached
Summary:	Memory ticket registry for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description integration-memcached
Memcached integration for CAS Server allows to store ticket registry
in memory cache.

%package integration-restlet
Summary:	I have no idea WTF is that, but it is for CAS server
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description integration-restlet
I really have no idea WTF is that. It name suggests it is yet another
registry storage driver for CAS, but it does not extends
AbstractDistributedTicketRegistry class.

%prep
%setup -q -n %{name}-server-%{version}
unzip modules/%{name}-server-webapp-%{version}.war -d webapp

sed -i 's,\(name="File" value="\)\([^"]*"\),\1%{logdir}/\2,' webapp/WEB-INF/classes/log4j.xml

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/%{name},%{_datadir},%{_sharedstatedir}/%{name},%{_tomcatconfdir},%{logdir}}

cp -a webapp $RPM_BUILD_ROOT%{webappdir}

MODULES="
  integration-berkeleydb
  integration-jboss
  integration-memcached
  integration-restlet
  support-generic
  support-jdbc
  support-ldap
  support-legacy
  support-openid
  support-radius
  support-spnego
  support-trusted
  support-x509
"

CONFIGFILES="
  classes/log4j.xml
  cas.properties
  deployerConfigContext.xml
  login-webflow.xml
  restlet-servlet.xml
  cas-servlet.xml
  web.xml
"

for i in $MODULES; do
  install modules/%{name}-server-$i-%{version}.jar $RPM_BUILD_ROOT%{libdir}/%{name}-$i-%{version}.jar
done

for i in $CONFIGFILES; do
  mv $RPM_BUILD_ROOT%{webappdir}/WEB-INF/$i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i)
  ln -s %{_sysconfdir}/%{name}/$(basename $i) $RPM_BUILD_ROOT%{webappdir}/WEB-INF/$i
done

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/tomcat-context.xml
ln -sf %{_sysconfdir}/%{name}/tomcat-context.xml $RPM_BUILD_ROOT%{_tomcatconfdir}/%{name}.xml

%postun
%tomcat_clear_cache %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.properties
%{_tomcatconfdir}/%{name}.xml
%{_datadir}/%{name}
%exclude %{libdir}/%{name}-support-spnego-%{version}.jar
%exclude %{libdir}/%{name}-integration-berkeleydb-%{version}.jar
%exclude %{libdir}/%{name}-support-x509-%{version}.jar
%exclude %{libdir}/%{name}-integration-jboss-%{version}.jar
%exclude %{libdir}/%{name}-support-openid-%{version}.jar
%exclude %{libdir}/%{name}-support-legacy-%{version}.jar
%exclude %{libdir}/%{name}-support-radius-%{version}.jar
%exclude %{libdir}/%{name}-integration-memcached-%{version}.jar
%exclude %{libdir}/%{name}-integration-restlet-%{version}.jar
%exclude %{libdir}/%{name}-support-ldap-%{version}.jar
%exclude %{libdir}/%{name}-support-generic-%{version}.jar
%exclude %{libdir}/%{name}-support-trusted-%{version}.jar
%exclude %{libdir}/%{name}-support-jdbc-%{version}.jar
%attr(2775,root,servlet) %dir %{_sharedstatedir}/%{name}
%dir %attr(2770,root,servlet) %{logdir}

%files authenticator-spnego
%defattr(644,root,root,755)
%{libdir}/%{name}-support-spnego-%{version}.jar

%files authenticator-x509
%defattr(644,root,root,755)
%{libdir}/%{name}-support-x509-%{version}.jar

%files authenticator-openid
%defattr(644,root,root,755)
%{libdir}/%{name}-support-openid-%{version}.jar

%files authenticator-legacy
%defattr(644,root,root,755)
%{libdir}/%{name}-support-legacy-%{version}.jar

%files authenticator-radius
%defattr(644,root,root,755)
%{libdir}/%{name}-support-radius-%{version}.jar

%files authenticator-ldap
%defattr(644,root,root,755)
%{libdir}/%{name}-support-ldap-%{version}.jar

%files authenticator-generic
%defattr(644,root,root,755)
%{libdir}/%{name}-support-generic-%{version}.jar

%files authenticator-trusted
%defattr(644,root,root,755)
%{libdir}/%{name}-support-trusted-%{version}.jar

%files authenticator-jdbc
%defattr(644,root,root,755)
%{libdir}/%{name}-support-jdbc-%{version}.jar

%files integration-berkeleydb
%defattr(644,root,root,755)
%{libdir}/%{name}-integration-berkeleydb-%{version}.jar

%files integration-jboss
%defattr(644,root,root,755)
%{libdir}/%{name}-integration-jboss-%{version}.jar

%files integration-memcached
%defattr(644,root,root,755)
%{libdir}/%{name}-integration-memcached-%{version}.jar

%files integration-restlet
%defattr(644,root,root,755)
%{libdir}/%{name}-integration-restlet-%{version}.jar
