%define name    mini_sendmail
%define version 1.3.5
%define release %mkrel 5
%define summary Accept email on behalf of real sendmail

Summary:	%summary
Name:		%name
Version:	%version
Release:	%release
License:	BSD
Group:		Networking/Mail
URL:		http://www.acme.com/software/mini_sendmail
Source0:	http://www.acme.com/software/mini_sendmail/%name-%version.tar.gz
Patch0:		%name-1.3.2-makefile.patch.bz2
Provides:	sendmail-command
BuildRoot:      %_tmppath/%name-buildroot

%description
mini_sendmail reads its standard input up to an end-of-file and sends a copy
of the message found there to all of the addresses listed. The message is sent
by connecting to a local SMTP server. This means mini_sendmail can be used to
send email from inside a chroot(2) area.

%prep 
%setup -q
%patch -p1 -b .makefile

%build
make mini_sendmail	PREFIX=%{_prefix} \
			BINDIR=%{_sbindir} \
			MANDIR=%{_mandir}

%install
%__mkdir_p %buildroot/%_docdir/%name-%version
%__mkdir_p %buildroot/%_sbindir/%name-%version

%__cp $RPM_BUILD_DIR/%name-%version/README %buildroot/%{_docdir}/%name-%version
%__cp $RPM_BUILD_DIR/%name-%version/FILES %buildroot/%{_docdir}/%name-%version
%__cp $RPM_BUILD_DIR/%name-%version/mini_sendmail %buildroot/%{_sbindir}/mini_sendmail

%clean
rm -rf %buildroot

%post
update-alternatives --install %{_sbindir}/sendmail sendmail-command %{_sbindir}/mini_sendmail 5

%preun
if [ $1 = 0 ]; then
	update-alternatives --remove sendmail-command %{_sbindir}/mini_sendmail
fi

%files
%defattr(-,root,root)
%doc README FILES
%_sbindir/mini_sendmail

