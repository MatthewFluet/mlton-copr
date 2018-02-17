Name:		mlton
Version:	20180207
Release:	4%{?dist}
Summary:	Whole-program optimizing compiler for Standard ML

Group:		Development/Languages
License:	MIT
URL:		http://mlton.org/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.src.tgz

# Set relative path of library directory to binary directory when installing mlton script
# Some systems (e.g., x86_64 Fedora) want to install the library files
# in /usr/lib64, rather than /usr/lib. Thus, when installing it is
# necessary to compute and set the relative path of TLIB to TBIN when
# installing $(TBIN)/mlton.
# Fixed upstream; this patch to be removed after next upstream release
Patch0:		https://github.com/MLton/mlton/pull/250.diff

# Use Unix newline for asciidoc output
# Fixed upstream; this patch to be removed after next upstream release
Patch1:		https://github.com/MLton/mlton/pull/251.diff

BuildRequires:	gcc gmp-devel mlton
Requires:	gcc gmp-devel


# Needs bootrap on these arches
ExcludeArch:	aarch64 %{power64} s390x


# filter out false dependencies
%{?filter_setup:
%filter_provides_in %{_docdir}
%filter_requires_in %{_docdir}
%filter_provides_in %{_libdir}/mlton/sml
%filter_requires_in %{_libdir}/mlton/sml
%filter_setup
}


%description
MLton is a whole-program optimizing compiler for Standard ML.  MLton
generates small executables with excellent runtime performance,
utilizing untagged and unboxed native integers, reals, and words,
unboxed native arrays, fast arbitrary-precision arithmetic based on
GnuMP, and multiple code generation and garbage collection strategies.
In addition, MLton provides a feature rich Standard ML programming
environment, with full support for SML97 as given in The Definition
of Standard ML (Revised), a number of useful language extensions, a
complete implementation of the Standard ML Basis Library, various
useful libraries, a simple and fast C foreign function interface, the
ML Basis system for programming with source libraries, and tools such
as a lexer generator, a parser generator, and a profiler.


%prep
%autosetup -p1
# quell rpmlint warnings: wrong-file-end-of-line-encoding
# Although "fixed" by Patch1, mlton-20180207.src.tgz ships with generated HTML
# (to allow downstream packaging to skip building documentation) that has DOS
# newlines.  The following converts DOS newlines to Unix newlines in the
# provided HTML (that will be installed via the `make install-docs` below.
# Fixed upstream; this shell command to be removed after next upstream release
( cd doc/guide/localhost ; find . -maxdepth 1 -type f -exec sed -i 's/\r$//' '{}' ';' )

%build
make CFLAGS="$RPM_OPT_FLAGS" all

%install
make DESTDIR=$RPM_BUILD_ROOT bindir=%{_bindir} libdir=%{_libdir} mandir=%{_mandir} docdir=%{_pkgdocdir} install-no-strip install-docs
# quell rpmlint errors: wrong-script-interpreter
for f in $RPM_BUILD_ROOT%{_bindir}/mlton $RPM_BUILD_ROOT%{_libdir}/mlton/static-library; do sed -i 's|/usr/bin/env bash|/bin/bash|' "$f"; done


%files
%{_bindir}/ml*
%{_libdir}/mlton
%{_mandir}/man1/*
%{_pkgdocdir}
%doc


%changelog
* Sat Feb 17 2018 Matthew Fluet <Matthew.Fluet@gmail.com> - 20180207-4
- Add upstream patch to use Unix newline for asciidoc output
- Add comments noting items fixed upstream and to be removed from spec file
  after next upstream release.

* Sat Feb 17 2018 Matthew Fluet <Matthew.Fluet@gmail.com> - 20180207-3
- Use autosetup -p1, rather than setup -q && patch -p1
- Revise description
- Fetch upstream patch to set relative path of library directory to binary
  directory when installing mlton script via pull-request diff
- Fix some rmplint warnings (wrong-file-end-of-line-encoding) and errors
  (wrong-script-interpreter)

* Thu Feb 15 2018 Matthew Fluet <Matthew.Fluet@gmail.com> - 20180207-2
- Add upstream patch to set relative path of library directory to binary
  directory when installing mlton script
- Use _bindir, _libdir, _mandir, and _pkgdocdir for make install

* Wed Feb 14 2018 Matthew Fluet <Matthew.Fluet@gmail.com> - 20180207-1
- New upstream release: http://mlton.org/Release20180207
- Drop patch to not call mprotect with PROT_EXEC; fixed upstream

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20130715-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 20130715-11
- Rebuild due to bug in RPM (RHBZ #1468476)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20130715-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep  6 2016 Peter Robinson <pbrobinson@fedoraproject.org> 20130715-9
- Add ExcludeArch until those arches are bootstrapped (rhbz 1056365)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20130715-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130715-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130715-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130715-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Sep 29 2013 Adam Goode <adam@spicenitz.org> - 20130715-4
- Fix recent regression of not using RPM_OPT_FLAGS #1013323

* Sat Sep 28 2013 Adam Goode <adam@spicenitz.org> - 20130715-3
- Use pkgdocdir instead of docdir

* Thu Sep 26 2013 Adam Goode <adam@spicenitz.org> - 20130715-2
- Switch to unversioned docdir

* Thu Sep 26 2013 Adam Goode <adam@spicenitz.org> - 20130715-1
- New upstream release: http://mlton.org/Release20130715

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100608-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Apr 27 2013 Adam Goode <adam@spicenitz.org> - 20100608-17
- MLton is too big for polyml, so bootstrap arm, armhfp, ppc, ppc64 with mlton
- Don't use htmldoc anymore, it often crashes
- Remove max-heap workaround

* Mon Apr 22 2013 Adam Goode <adam@spicenitz.org> - 20100608-16
- Scrap all the arch-specific bootstrapping, use polyml to do it

* Sun Apr 21 2013 Adam Goode <adam@spicenitz.org> - 20100608-15
- Try a more generalized bootstrap approach

* Sat Apr 20 2013 Adam Goode <adam@spicenitz.org> - 20100608-14
- Really fix builds by more intelligently setting max-heap

* Sat Apr 20 2013 Adam Goode <adam@spicenitz.org> - 20100608-13
- Fix ppc64 bootstrap

* Sat Apr 20 2013 Adam Goode <adam@spicenitz.org> - 20100608-12
- Bootstrap ppc64

* Fri Apr 19 2013 Adam Goode <adam@spicenitz.org> - 20100608-11
- Bootstrap ppc

* Thu Apr 18 2013 Adam Goode <adam@spicenitz.org> - 20100608-10
- Constrain max-heap to a fixed value during building, otherwise 70% of physical
  ram is used
- Fix detection of ppc64

* Mon Apr 15 2013 Adam Goode <adam@spicenitz.org> - 20100608-9
- Fix for #914188 FTBFS
- Update source link
- Remove ExclusiveArch, per packaging recommendations

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100608-8.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100608-7.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100608-6.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Marcela Mašláňová <mmaslano@redhat.com> - 20100608-5.2
- rebuild with new gmp without compat lib

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 20100608-5.1
- rebuild with new gmp

* Fri Aug 12 2011 Adam Goode <adam@spicenitz.org> - 20100608-5
- Clean up auto dependences

* Fri Mar 11 2011 Dan Horák <dan[at]danny.cz> - 20100608-4
- set ExclusiveArch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20100608-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jun 11 2010 Adam Goode <adam@spicenitz.org> - 20100608-2
- Change location of upstream source

* Fri Jun 11 2010 Adam Goode <adam@spicenitz.org> - 20100608-1
- New upstream release, see http://mlton.org/Release20100608

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20070826-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Adam Goode <adam@spicenitz.org> - 20070826-19
- Add forgotten changelog entry

* Sun May 31 2009 Adam Goode <adam@spicenitz.org> - 20070826-18
- ARM is bootstrapped, build again

* Sun May 31 2009 Adam Goode <adam@spicenitz.org> - 20070826-17
- Use non-trunk version of MLton to bootstrap ARM

* Tue May 26 2009 Adam Goode <adam@spicenitz.org> - 20070826-16
- Add missing ARM patch

* Tue May 26 2009 Adam Goode <adam@spicenitz.org> - 20070826-15
- Bootstrap ARM

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20070826-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 30 2008 Adam Goode <adam@spicenitz.org> - 20070826-13
- RPM 4.6 fix for patch tag
- Update LaTeX build requires

* Sat Feb  9 2008 Adam Goode <adam@spicenitz.org> - 20070826-12
- Introduce patch to not call mprotect with PROT_EXEC

* Fri Jan 18 2008 Adam Goode <adam@spicenitz.org> - 20070826-11
- Rebuild for new GCC

* Thu Sep 27 2007 Adam Goode <adam@spicenitz.org> - 20070826-10
- Disable bootstrap

* Thu Sep 27 2007 Adam Goode <adam@spicenitz.org> - 20070826-9
- Re-bootstrap ppc

* Wed Sep 26 2007 Adam Goode <adam@spicenitz.org> - 20070826-8
- Really fix SRPM conditionals

* Wed Sep 26 2007 Adam Goode <adam@spicenitz.org> - 20070826-7
- Work around strange SRPM problem in conditionals
- Fix changelog (forgot release 5?)

* Wed Sep 26 2007 Adam Goode <adam@spicenitz.org> - 20070826-6
- Build on ppc now that #247407 is fixed

* Thu Sep 13 2007 Adam Goode <adam@spicenitz.org> - 20070826-4
- Do not condition bootstrap source tag

* Thu Sep 13 2007 Adam Goode <adam@spicenitz.org> - 20070826-3
- Bootstrap x86_64

* Mon Aug 27 2007 Adam Goode <adam@spicenitz.org> - 20070826-2
- Exclude ppc for now (GCC internal compiler error!)

* Sun Aug 26 2007 Adam Goode <adam@spicenitz.org> - 20070826-1
- Update to new release

* Wed Aug 22 2007 Adam Goode <adam@spicenitz.org> - 20061107-4
- Exclude ppc64 for now

* Wed Aug 22 2007 Adam Goode <adam@spicenitz.org> - 20061107-3
- Update license tag
- Rebuild for buildid

* Fri Nov 24 2006 Adam Goode <adam@spicenitz.org> - 20061107-2
- Use RPM_OPT_FLAGS
- Correctly instantiate version
- Adjust patches

* Sun Nov 12 2006 Adam Goode <adam@spicenitz.org> - 20061107-1
- New release, taken from svn://mlton.org/mlton/tags/on-20061107

* Thu Aug 31 2006 Adam Goode <adam@spicenitz.org> - 20051202-8.1
- Mass rebuild

* Sun Jul  9 2006 Adam Goode <adam@spicenitz.org> - 20051202-8
- Conditionalize bootstrapping and disable it

* Sat Jul  1 2006 Adam Goode <adam@spicenitz.org> - 20051202-7
- Fix macro in changelog
- Remove mixed use of tabs and spaces

* Sun Jun 25 2006 Adam Goode <adam@spicenitz.org> - 20051202-6
- Build runtime with -g, but not -gstabs+
- Re-enable debuginfo packages

* Wed Jun 21 2006 Adam Goode <adam@spicenitz.org> - 20051202-5
- Disable empty debuginfo packages

* Wed Jun 21 2006 Adam Goode <adam@spicenitz.org> - 20051202-4
- Be more specific about license
- Add "which" to BuildRequires until everyone is running new mock

* Tue Jun 20 2006 Adam Goode <adam@spicenitz.org> - 20051202-3
- Create PDF documentation for mlyacc and mllex (instead of .ps.gz)
- Move ckit-lib/doc and smlnj-lib/Doc to %%{_docdir}
- Remove regression files from ckit

* Thu Jun  8 2006 Adam Goode <adam@spicenitz.org> - 20051202-2
- Change to use bootstrap

* Wed Jun  7 2006 Adam Goode <adam@spicenitz.org> - 20051202-1
- Initial release for FC5
