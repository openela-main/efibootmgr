%define efivar_version 35-1

Summary: EFI Boot Manager
Name: efibootmgr
Version: 16
Release: 1%{?dist}
Group: System Environment/Base
License: GPLv2+
URL: http://github.com/rhinstaller/%{name}/
BuildRequires: git, popt-devel
BuildRequires: efivar-libs >= %{efivar_version}
BuildRequires: efivar-devel >= %{efivar_version}
# EFI/UEFI don't exist on PPC
ExclusiveArch: %{ix86} x86_64 aarch64 arm

# for RHEL / Fedora when efibootmgr was part of the elilo package
Conflicts: elilo <= 3.6-6
Obsoletes: elilo <= 3.6-6

Source0: https://github.com/rhinstaller/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2

%global efidir %(eval echo $(grep ^ID= /etc/os-release | sed -e 's/^ID=//' -e 's/rhel/redhat/'))

%description
%{name} displays and allows the user to edit the Intel Extensible
Firmware Interface (EFI) Boot Manager variables.  Additional
information about EFI can be found at
http://developer.intel.com/technology/efi/efi.htm and http://uefi.org/.

%prep
%setup -q
git init
git config user.email "example@example.com"
git config user.name "RHEL Ninjas"
git add .
git commit -a -q -m "%{version} baseline."
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
make %{?_smp_mflags} CFLAGS='%{optflags}' LDFLAGS='%{build_ldflags}' \
  EFIDIR=%{efidir}

%install
rm -rf %{buildroot}
%make_install EFIDIR=%{efidir} libdir=%{_libdir} \
       bindir=%{_bindir} mandir=%{_mandir} localedir=%{_datadir}/locale/ \
       includedir=%{_includedir} libexecdir=%{_libexecdir} \
       datadir=%{_datadir}

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/*
%{_mandir}/*/*.?.gz
%doc README
    
%changelog
* Mon Apr 09 2018 Peter Jones <pjones@redhat.com> - 16-1
- efibootmgr 16
- better coverity and clang-analyzer support
- better CI
- minor fixes

* Tue Feb 27 2018 Peter Jones <pjones@redhat.com> - 15-6
- Rebuild against newer efivar.

* Fri Feb 23 2018 Florian Weimer <fweimer@redhat.com> - 15-5
- Use CFLAGS & LDFLAGS from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 08 2017 Peter Jones <pjones@redhat.com> - 15-1
- Update to efibootmgr 15
- Make efibootmgr use EFIDIR / efibootmgr.efidir like fwupdate does
- make --loader default build-time configurable
- sanitize set_mirror()/get_mirror()
- Add support for parsing loader options as UCS2
- GCC 7 fixes
- Don't use -fshort-wchar since we don't run on EFI machines.
- Also rebuild for efivar-31-1.fc26 to get symbol versioning right.
  Resolves: rhbz#1468841

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 28 2016 Peter Jones <pjones@redhat.com> - 14-3
- Rebuild for efivar-30-3, this time with the right library sonames.

* Wed Sep 28 2016 Peter Jones <pjones@redhat.com> - 14-2
- Rebuild for efivar-30-2

* Tue Sep 27 2016 Peter Jones <pjones@redhat.com> - 14-1
- Update to efibootmgr 14
- Remove "(hex)" from description of --delete-bootnum
- Fix a typo in the popt options
- Add README.md
- make efibootdump install by default
- Man page fixes
- Better compiler detection
- Don't use --default-symver in efibootmgr
- Make -flto part of the overrideable CFLAGS

* Wed Aug 17 2016 Peter Jones <pjones@redhat.com> - 13-2
- Update to efibootmgr 13
- Add support for --sysprep and --driver to support UEFI System Prep
  Applications and UEFI Drivers.
- use efivar's error reporting facility, and show error traces when
  "-v -v" is used.
- Still yet better error codes returned on failures.
- Add -m and -M to support Memory Address Range Mirroring.
- Add efibootdump, to examine Boot* variables found in tarballs in bug
  reports and similar.
- miscellaneous bugfixes.

* Thu Aug 11 2016 Peter Jones <pjones@redhat.com> - 13-1
- Update to version 13
- add efibootdump
- use efivar's error reporting facility
- Add address range mirroring support
- lots of bug fixes

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Peter Jones <pjones@redhat.com> - 0.12-1
- Update to 0.12
- use libefiboot and libefivar to make device paths and load options
- don't depend on -lz or -lpci any more

* Tue Oct 21 2014 Peter Jones <pjones@redhat.com> - 0.11.0-1
- Fix "-n" and friends not being assigned/checked right sometimes from 0.10.0-1
- Generate more archives to avoid people using github's, because they're just
  bad.

* Mon Oct 20 2014 Peter Jones <pjones@redhat.com> - 0.10.0-1
- Make -o parameter validation work better and be more informative
- Better exit values
- Fix a segfault with appending ascii arguments.

* Tue Sep 09 2014 Peter Jones <pjones@redhat.com> - 0.8.0-1
- Release 0.8.0

* Mon Jan 13 2014 Peter Jones <pjones@redhat.com> - 0.6.1-1
- Release 0.6.1

* Mon Jan 13 2014 Jared Dominguez <Jared_Dominguez@dell.com>
- new home https://github.com/vathpela/efibootmgr

* Thu Jan  3 2008 Matt Domsch <Matt_Domsch@dell.com> 0.5.4-1
- split efibootmgr into its own RPM for Fedora/RHEL.

* Tue Aug 24 2004 Matt Domsch <Matt_Domsch@dell.com>
- new home linux.dell.com

* Fri May 18 2001 Matt Domsch <Matt_Domsch@dell.com>
- See doc/ChangeLog
