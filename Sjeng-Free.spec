Summary:	Chess program that plays many variants
Name:		Sjeng-Free
Version:	11.2
Release:	1
License:	GPL v2
Group:		Applications/Games/Boards
Source0:	http://www.sjeng.org/ftp/%{name}-%{version}.tar.gz
# Source0-md5:	6561e740b7af703c16701304697d2870
Source1:	%{name}.6
Source2:	%{name}-README
Patch0:		%{name}-cleanup.patch.bz2
Patch1:		%{name}-FHS.patch.bz2
URL:		http://sjeng.org/
BuildRequires:	automake
BuildRequires:	gdbm-devel
Provides:	chess_backend
Buildroot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Sjeng is a chess program that plays normal chess and many variants
like crazyhouse, bughouse, suicide (aka giveaway or anti-chess) and
losers. It can also play variants which have the same rules as normal
chess, but a different starting position. It uses the XBoard/WinBoard
interface by Tim Mann, so it can be used with xboard or eboard. It is
also capable of playing on internet chess servers.

%prep
%setup -q
%patch0 -p1 -b .cleanup
%patch1 -p1 -b .fhs
cp %{SOURCE2} README.debian

# (Abel) supress annoying rpmlint warning message
%{__perl} -pi -e 's/\r//g' [[:upper:]][[:upper:]]* ChangeLog

%build
autoreconf --force --install
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d ${RPM_BUILD_ROOT}{%{_datadir}/sjeng,%{_sysconfdir},%{_mandir}/man6}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install sjeng.rc ${RPM_BUILD_ROOT}%{_sysconfdir}
install books/*.opn ${RPM_BUILD_ROOT}%{_datadir}/sjeng
install %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man6/sjeng.6

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog NEWS README* THANKS tests/*.epd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sjeng.rc
%attr(755,root,root) %{_bindir}/sjeng
%dir %{_datadir}/sjeng
%{_datadir}/sjeng/*.opn
%{_mandir}/man6/*.6*
