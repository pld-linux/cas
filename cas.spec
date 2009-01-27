%include	/usr/lib/rpm/macros.java
Summary:	JA-SIG Central Authentication Service
Name:		cas-server
Version:	3.3.1
Release:	0.1
License:	MIT License
Group:		Development/Languages/Java
Source0:	http://www.ja-sig.org/downloads/cas/%{name}-%{version}-release.tar.gz
# Source0-md5:	2b7df2a84e12b045c5accc987f94f169
URL:		http://www.ja-sig.org/products/cas/
BuildRequires:	jpackage-utils
BuildRequires:	maven
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
# Require version that uses tomcat uid/gid
Requires:	apache-tomcat >= 5.5.27-0.2
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
CAS is an authentication system originally created by Yale University
to provide a trusted way for an application to authenticate a user.
CAS became a JA-SIG project in December 2004.

CAS provides enterprise single sign on service: CAS Downloads

    - An open and well-documented protocol
    - An open-source Java server component
    - A library of clients for Java, .Net, PHP, Perl, Apache, uPortal, and
      others
    - Integrates with uPortal, BlueSocket, TikiWiki, Mule, Liferay, Moodle
      and others
    - Community documentation and implementation support
    - An extensive community of adopters
%prep
%setup -q

%build
mvn package install

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/cas-server,%{_datadir}/tomcat/webapps/cas-server,%{_sharedstatedir}/{cas-server,tomcat/conf/Catalina/localhost}}
cp -a . $RPM_BUILD_ROOT%{_datadir}/tomcat/webapps/cas-server
ln -sf %{_sysconfdir}/cas-server/web.xml $RPM_BUILD_ROOT%{_datadir}/tomcat/webapps/cas-server/WEB-INF/web.xml

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/cas-server
%config(noreplace) %{_sysconfdir}/cas-server/web.xml
# do not make this file writeable by tomcat. We do not want to allow user to
# undeploy this app via tomcat manager.
%config(noreplace) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/cas-server.xml
%{_datadir}/tomcat/webapps/cas-server
%attr(755,tomcat,tomcat) %dir %{_sharedstatedir}/cas-server