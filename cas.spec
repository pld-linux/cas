%include	/usr/lib/rpm/macros.java
Summary:	JA-SIG Central Authentication Service
Name:		cas-server
Version:	3.3.5
Release:	0.1
License:	MIT License
Group:		Networking/Daemons/Java/Servlets
Source0:	http://www.ja-sig.org/downloads/cas/%{name}-%{version}-release.tar.gz
# Source0-md5:	c12594a2af98ee2dd11a8c97895d91af
Source1:	%{name}-context.xml
URL:		http://www.ja-sig.org/products/cas/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.540
Requires:	jpackage-utils
Requires:	tomcat >= 6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define webappdir %{_datadir}/%{name}
%define libdir    %{_datadir}/%{name}/WEB-INF/lib

%description
CAS is an authentication system originally created by Yale University
to provide a trusted way for an application to authenticate a user.
CAS became a JA-SIG project in December 2004.

CAS provides enterprise single sign on service. It features:

- An open and well-documented protocol
- An open-source Java server component
- A library of clients for Java, .Net, PHP, Perl, Apache, uPortal
  and others
- Integrates with uPortal, BlueSocket, TikiWiki, Mule, Liferay, Moodle
  and others
- Community documentation and implementation support
- An extensive community of adopters

%package authenticator-spnego
Summary:	Spnego authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-spnego
Spnego authentication backend for CAS Server.

%package authenticator-x509
Summary:	x509 authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-x509
X509 client certificates authentication backend for CAS Server.

%package authenticator-openid
Summary:	OpenID authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-openid
OpenID authentication backend for CAS Server.

%package authenticator-legacy
Summary:	Legacy authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-legacy
Legacy authentication backend for CAS Server.

%package authenticator-radius
Summary:	Radius authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-radius
Radius authentication backend for CAS Server.

%package authenticator-ldap
Summary:	LDAP authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-ldap
LDAP authentication backend for CAS Server.

%package authenticator-generic
Summary:	Generic authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-generic
Generic authentication backend for CAS Server.

%package authenticator-trusted
Summary:	Trusted authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-trusted
Trusted authentication backend for CAS Server.

%package authenticator-jdbc
Summary:	JDBC authenticator for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description authenticator-jdbc
JDBC authentication backend for CAS Server.

%package integration-berkeleydb
Summary:	Berkeleydb ticket registry for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description integration-berkeleydb
BerkeleyDB integration for CAS Server allows to store ticket registry
in berkeleyDB.

%package integration-jboss
Summary:	Jboss ticket registry for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description integration-jboss
Jboss integration for CAS Server allows to store ticket registry in
Jboss internal authentication system.

%package integration-memcached
Summary:	Memory ticket registry for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description integration-memcached
Memcached integration for CAS Server allows to store ticket registry
in memory cache.

%package integration-restlet
Summary:	 I have no idea WTF is that, but it is for CAS server
Requires:	%{name} = %{version}-%{release}
Group:		Libraries/Java

%description integration-restlet
I really have no idea WTF is that. It name suggests it is yet another
registry storage driver for CAS, but it does not extends
AbstractDistributedTicketRegistry class.

%prep
%setup -q
unzip modules/%{name}-webapp-%{version}.war -d webapp

%build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/cas-server,%{_datadir},%{_sharedstatedir}/cas-server,%{_tomcatconfdir}}

cp -a webapp $RPM_BUILD_ROOT%{webappdir}

MODULES="integration-berkeleydb
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
support-x509"

for i in $MODULES; do
  install modules/%{name}-$i-%{version}.jar $RPM_BUILD_ROOT%{libdir}/%{name}-$i-%{version}.jar
done

install %{SOURCE1} $RPM_BUILD_ROOT%{_tomcatconfdir}/cas-server.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %{_tomcatconfdir}/cas-server.xml
%{_datadir}/cas-server
%exclude %{libdir}/cas-server-support-spnego-3.3.5.jar
%exclude %{libdir}/cas-server-integration-berkeleydb-3.3.5.jar
%exclude %{libdir}/cas-server-support-x509-3.3.5.jar
%exclude %{libdir}/cas-server-integration-jboss-3.3.5.jar
%exclude %{libdir}/cas-server-support-openid-3.3.5.jar
%exclude %{libdir}/cas-server-support-legacy-3.3.5.jar
%exclude %{libdir}/cas-server-support-radius-3.3.5.jar
%exclude %{libdir}/cas-server-integration-memcached-3.3.5.jar
%exclude %{libdir}/cas-server-integration-restlet-3.3.5.jar
%exclude %{libdir}/cas-server-support-ldap-3.3.5.jar
%exclude %{libdir}/cas-server-support-generic-3.3.5.jar
%exclude %{libdir}/cas-server-support-trusted-3.3.5.jar
%exclude %{libdir}/cas-server-support-jdbc-3.3.5.jar
%attr(2755,root,servlet) %dir %{_sharedstatedir}/cas-server

%files authenticator-spnego
%defattr(644,root,root,755)
%{libdir}/cas-server-support-spnego-3.3.5.jar

%files authenticator-x509
%defattr(644,root,root,755)
%{libdir}/cas-server-support-x509-3.3.5.jar

%files authenticator-openid
%defattr(644,root,root,755)
%{libdir}/cas-server-support-openid-3.3.5.jar

%files authenticator-legacy
%defattr(644,root,root,755)
%{libdir}/cas-server-support-legacy-3.3.5.jar

%files authenticator-radius
%defattr(644,root,root,755)
%{libdir}/cas-server-support-radius-3.3.5.jar

%files authenticator-ldap
%defattr(644,root,root,755)
%{libdir}/cas-server-support-ldap-3.3.5.jar

%files authenticator-generic
%defattr(644,root,root,755)
%{libdir}/cas-server-support-generic-3.3.5.jar

%files authenticator-trusted
%defattr(644,root,root,755)
%{libdir}/cas-server-support-trusted-3.3.5.jar

%files authenticator-jdbc
%defattr(644,root,root,755)
%{libdir}/cas-server-support-jdbc-3.3.5.jar

%files integration-berkeleydb
%defattr(644,root,root,755)
%{libdir}/cas-server-integration-berkeleydb-3.3.5.jar

%files integration-jboss
%defattr(644,root,root,755)
%{libdir}/cas-server-integration-jboss-3.3.5.jar

%files integration-memcached
%defattr(644,root,root,755)
%{libdir}/cas-server-integration-memcached-3.3.5.jar

%files integration-restlet
%defattr(644,root,root,755)
%{libdir}/cas-server-integration-restlet-3.3.5.jar
