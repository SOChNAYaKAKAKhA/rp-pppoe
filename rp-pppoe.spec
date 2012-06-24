Summary:	PPP Over Ethernet client
Summary(pl):	Klient PPP Poprzez Ethernet (PPPoE)
Summary(pt_BR):	Protocolo PPPoE (PPP over Ethernet), usado comumente com modens xDSL
Summary(ru):	PPP Over Ethernet (��������� xDSL)
Summary(uk):	PPP Over Ethernet (Ц������� xDSL)
Name:		rp-pppoe
Version:	3.7
Release:	1
License:	GPL v2+
Group:		Networking
Source0:	http://www.roaringpenguin.com/penguin/pppoe/%{name}-%{version}.tar.gz
# Source0-md5:	32c34455ccdfd9610304479e1beac3ff
Source1:	%{name}-server.init
Source2:	%{name}-server.sysconfig
Source3:	%{name}-relay.init
Source4:	%{name}-relay.sysconfig
Patch0:		%{name}-ac.patch
Patch1:		%{name}-tkpppoe.in.patch
Patch2:		%{name}-plugins.patch
URL:		http://www.roaringpenguin.com/pppoe/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	ppp >= 2.4.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PPPoE (Point-to-Point Protocol over Ethernet) is a protocol used by
many ADSL Internet Service Providers. Roaring Penguin has a free
client for Linux systems to connect to PPPoE service providers.

The client is a user-mode program and does not require any kernel
modifications. It is fully compliant with RFC 2516, the official PPPoE
specification.

%description -l pl
PPPoE (Protok� Punkt-Punkt poprzez Ethernet) jest protoko�em u�ywanym
przez wielu dostarczycieli us�ugi ADSL.

Klient jest programem dzia�aj�cym w przestrzeni u�ytkownika, a to
oznacza, �e nie wymaga modyfikacji kernela. Jest w pe�ni zgodny z
oficjaln� specyfikacj� PPPoE - RFC 2516.

%description -l pt_BR
PPPoE (Point-to-Point Protocol over Ethernet) � um protocolo usado por
muitos provedores de acesso � internet e companhias telef�nicas para
prover acesso de alta velocidade xDSL.

Este cliente � um programa user-mode que n�o necessita de modifica��es
no kernel. Esta implementa��o segue a RFC 2516, a especifica��o
oficial para PPPoE.

%description -l ru
PPPoE (Point-to-Point Protocol over Ethernet) - ��� ��������,
������������ ������� ADSL ISP. Roaring Penguin �������������
������������������������� ������� ��� ����������� � ����� ISP.

������ ������������ ����� ��������� ���������������� ��������� � ��
������� �����-���� ����������� ����. �� ��������� ��������� � RFC
2516, ����������� ������������� PPPoE.

%description -l uk
PPPoE (Point-to-Point Protocol over Ethernet) - �� ��������, ����
����������դ���� �������� ADSL ISP. Roaring Penguin ����� צ������
�̦���� ��� Ц��������� �� ����� ISP.

�̦��� ���Ѥ ����� ���Φ��� ������������� �������� � �� �������
����-���� ����Ʀ��æ� ����. ��� ���Φ��� ��ͦ���� � RFC 2516,
�Ʀæ������ �����Ʀ��æ�� PPPoE.

%package gui
Summary:	GUI front-end for rp-pppoe
Summary(pl):	Graficzny interfejs dla rp-pppoe
Summary(pt_BR):	Interface gr�fica para configura��o do rp-pppoe
Group:		X11/Applications/Networking
Requires:	rp-pppoe >= 3.4

%description gui
This package contains the graphical frontend (Tk-based) for rp-pppoe.

%description gui -l pl
Graficzny interfejs u�ytkownika (oparty na Tk) dla rp-pppoe.

%description gui -l pt_BR
Este pacote fornece uma interface gr�fica para a configura��o do
rp-pppoe.

%package server
Summary:	PPPoE server
Summary(pl):	Serwer PPPoE
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	ppp >= 2.4.1
Requires:	rc-scripts

%description server
PPP over Ethernet server.

%description server -l pl
Serwer PPP over Ethernet.

%package relay
Summary:	PPPoE relay
Summary(pl):	Agent przekazuj�cy pakiety PPPoE
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description relay
PPP over Ethernet relay.

%description relay -l pl
Agent przekazuj�cy pakiety PPPoE.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
%{__aclocal}
%{__autoconf}
%configure
# we always want kernel mode PPPoE support in utilities
echo '#define HAVE_LINUX_KERNEL_PPPOE 1' >> config.h
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/{sysconfig,rc.d/init.d}

%{__make} -C src install \
	RPM_INSTALL_ROOT=$RPM_BUILD_ROOT
%{__make} -C gui install \
	RPM_INSTALL_ROOT=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/pppoe-server
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/pppoe-server
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/pppoe-relay
install %{SOURCE4} $RPM_BUILD_ROOT/etc/sysconfig/pppoe-relay

# This is necessary for the gui to work, but it shouldn't be done here !
install -d $RPM_BUILD_ROOT%{_sysconfdir}/ppp/rp-pppoe-gui

%clean
rm -fr $RPM_BUILD_ROOT

%post server
/sbin/chkconfig --add pppoe-server
%service pppoe-server restart "PPPoE daemon"

%preun server
if [ "$1" = "0" ]; then
	%service pppoe-server stop
	/sbin/chkconfig --del pppoe-server
fi

%post relay
/sbin/chkconfig --add pppoe-relay
%service pppoe-relay restart "PPPoE relay daemon"

%preun relay
if [ "$1" = "0" ]; then
	%service pppoe-relay stop
	/sbin/chkconfig --del pppoe-relay
fi

%files
%defattr(644,root,root,755)
%doc README doc/*
%attr(755,root,root) %{_sbindir}/pppoe
%attr(755,root,root) %{_sbindir}/pppoe-connect
%attr(755,root,root) %{_sbindir}/pppoe-setup
%attr(755,root,root) %{_sbindir}/pppoe-sniff
%attr(755,root,root) %{_sbindir}/pppoe-st*

%config(noreplace) %{_sysconfdir}/ppp/pppoe.conf
%config(noreplace) %{_sysconfdir}/ppp/firewall-masq
%config(noreplace) %{_sysconfdir}/ppp/firewall-standalone
%{_mandir}/man5/pppoe.conf.*
%{_mandir}/man8/pppoe-connect*
%{_mandir}/man8/pppoe-setup*
%{_mandir}/man8/pppoe-sniff*
%{_mandir}/man8/pppoe-st*
%{_mandir}/man8/pppoe.*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/tkpppoe
%attr(755,root,root) %{_sbindir}/pppoe-wrapper
%dir %{_sysconfdir}/ppp/rp-pppoe-gui
%{_datadir}/tkpppoe
%{_mandir}/man1/*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pppoe-server
%config(noreplace) %{_sysconfdir}/ppp/pppoe-server-options
%{_mandir}/man8/pppoe-server*
%attr(754,root,root) /etc/rc.d/init.d/pppoe-server
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pppoe-server

%files relay
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/pppoe-relay
%{_mandir}/man8/pppoe-relay*
%attr(754,root,root) /etc/rc.d/init.d/pppoe-relay
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/pppoe-relay
