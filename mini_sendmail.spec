%define name    mini_sendmail
%define version 1.3.6
%define release 2
%define summary Accept email on behalf of real sendmail

Summary:	%summary
Name:		%name
Version:	%version
Release:	%release
License:	BSD
Group:		Networking/Mail
URL:		https://www.acme.com/software/mini_sendmail
Requires(post,preun): update-alternatives
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
%patch0 -p1 -b .makefile

%build
make mini_sendmail	PREFIX=%{_prefix} \
			BINDIR=%{_sbindir} \
			MANDIR=%{_mandir}

%install
%__mkdir_p %buildroot/%_sbindir/
install mini_sendmail %buildroot/%{_sbindir}/mini_sendmail

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



%changelog
* Thu Mar 15 2012 Alexander Khrukin <akhrukin@mandriva.org> 1.3.6-1mdv2011.0
+ Revision: 785057
- version update 1.3.6
- version update 1.3.6

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.3.5-7mdv2009.0
+ Revision: 252533
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 1.3.5-5mdv2008.1
+ Revision: 133078
- requires update-alternatives
- simplify installing
- do not reinvent %%doc
- kill re-definition of %%buildroot on Pixel's request
- import mini_sendmail

