%define major 2
%define umajor 0
%define oldposixlib %mklibname pcre2-posix 1
%define posixlib %mklibname pcre2-posix %{major}
%define u8lib %mklibname pcre2-8 %{umajor}
%define u16lib %mklibname pcre2-16 %{umajor}
%define u32lib %mklibname pcre2-32 %{umajor}
%define dev %mklibname -d pcre2
%define static %mklibname -d -s pcre2

# (tpg) optimize a bit
%global optflags %{optflags} -Ofast

# This is stable release:
#%%global rcversion RC1
Name:		pcre2
Version:	10.31
Release:	%{?rcversion:0.}3%{?rcversion:.%rcversion}
%global		myversion %{version}%{?rcversion:-%rcversion}
Summary:	Perl-compatible regular expression library
Group:		System/Libraries
# the library:                          BSD
# pcre2test (linked to GNU readline):   BSD (linked to GPLv3+)
# COPYING:                              see LICENCE file
# LICENSE:                              BSD text and declares Public Domain
#                                       for testdata
#Not distributed in binary package
# aclocal.m4:                           FSFULLR and GPLv2+ with exception
# ar-lib:                               GPLv2+ with exception
# autotools:                            GPLv3+ with exception
# compile:                              GPLv2+ with exception
# config.sub:                           GPLv3+ with exception
# depcomp:                              GPLv2+ with exception
# install-sh:                           MIT
# ltmain.sh:                            GPLv2+ with exception and GPLv3+ with
#                                       exception and GPLv3+
# m4/ax_pthread.m4:                     GPLv3+ with exception
# m4/libtool.m4:                        FSFULLR and GPLv2+ with exception
# m4/ltoptions.m4:                      FSFULLR
# m4/ltsugar.m4:                        FSFULLR
# m4/ltversion.m4:                      FSFULLR
# m4/lt~obsolete.m4:                    FSFULLR
# m4/pcre2_visibility.m4:               FSFULLR
# missing:                              GPLv2+ with exception
# test-driver:                          GPLv2+ with exception
# testdata:                             Public Domain
License:	BSD
URL:		http://www.pcre.org/
Source0:	ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{?rcversion:Testing/}%{name}-%{myversion}.tar.bz2
# Do no set RPATH if libdir is not /usr/lib
Patch0:		pcre2-10.10-Fix-multilib.patch
BuildRequires:	readline-devel
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(zlib)

%description
PCRE2 is a re-working of the original PCRE (Perl-compatible regular
expression) library to provide an entirely new API.

PCRE2 is written in C, and it has its own API. There are three sets of
functions, one for the 8-bit library, which processes strings of bytes, one
for the 16-bit library, which processes strings of 16-bit values, and one for
the 32-bit library, which processes strings of 32-bit values. There are no C++
wrappers. This package provides support for strings in 8-bit and UTF-8
encodings. Install %{name}-utf16 or %{name}-utf32 packages for the other ones.

The distribution does contain a set of C wrapper functions for the 8-bit
library that are based on the POSIX regular expression API (see the pcre2posix
man page). These can be found in a library called libpcre2posix. Note that
this just provides a POSIX calling interface to PCRE2; the regular expressions
themselves still follow Perl syntax and semantics. The POSIX API is
restricted, and does not give full access to all of PCRE2's facilities.

%files
%{_bindir}/pcre2grep
%{_bindir}/pcre2test
%{_mandir}/man1/pcre2grep.*
%{_mandir}/man1/pcre2test.*

%package -n %{posixlib}
Summary:	Version of the PCRE2 library providing a POSIX-like regex API
Group:		System/Libraries
%rename %{oldposixlib}

%description -n %{posixlib}
Version of the PCRE2 library providing a POSIX-like regex API.

%files -n %{posixlib}
%{_libdir}/libpcre2-posix.so.%{major}*

%package -n %{u8lib}
Summary:	UTF-8 version of the PCRE2 library
Group:		System/Libraries
# GOT: julia-0.6.0-0.1.pre.alpha-omv2015.0.x86_64
# GOT: lib64pcre2-8_0-10.31-2-omv2015.0.x86_64
# In order to satisfy the 'libpcre2-8.so.0()(64bit)' dependency, one of the following packages is needed:
# 1- julia-0.6.0-0.1.pre.alpha-omv2015.0.x86_64: High-level, high-performance dynamic language for technical computing (to install)
# 2- lib64pcre2-8_0-10.31-2-omv2015.0.x86_64: UTF-8 version of the PCRE2 library (to install)
# What is your choice? (1-2)
Conflicts:	julia < 0.6.0-1

%description -n %{u8lib}
UTF-8 version of the PCRE2 library.

%files -n %{u8lib}
%{_libdir}/libpcre2-8.so.%{umajor}*

%package -n %{u16lib}
Summary:	UTF-16 version of the PCRE2 library
Group:		System/Libraries

%description -n %{u16lib}
UTF-16 version of the PCRE2 library.

%files -n %{u16lib}
%{_libdir}/libpcre2-16.so.%{umajor}*

%package -n %{u32lib}
Summary:	UTF-32 version of the PCRE2 library
Group:		System/Libraries

%description -n %{u32lib}
UTF-32 version of the PCRE2 library.

%files -n %{u32lib}
%{_libdir}/libpcre2-32.so.%{umajor}*

%package -n %{dev}
Summary:	Development files for the PCRE2 library
Group:		Development/C
Requires:	%{posixlib} = %{EVRD}
Requires:	%{u8lib} = %{EVRD}
Requires:	%{u16lib} = %{EVRD}
Requires:	%{u32lib} = %{EVRD}

%description -n %{dev}
Development files for the PCRE2 library.

%files -n %{dev}
%{_libdir}/*.so
%{_includedir}/*.h
%{_libdir}/pkgconfig/*
%{_mandir}/man1/pcre2-config.*
%{_mandir}/man3/*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c

%package -n %{static}
Summary:	Static library for linking to PCRE2
Group:		Development/C
Requires:	%{dev} = %{EVRD}

%description -n %{static}
Static library for linking to PCRE2.

%files -n %{static}
%{_libdir}/*.a

%prep
%setup -q -n %{name}-%{myversion}
%apply_patches
# Because of multilib patch
libtoolize --copy --force
autoreconf -vif

%build
# There is a strict-aliasing problem on PPC64, bug #881232
%ifarch ppc64
%global optflags %{optflags} -fno-strict-aliasing
%endif
%configure \
%ifarch s390 s390x sparc64 sparcv9 riscv64
    --disable-jit \
    --disable-pcre2grep-jit \
%else
    --enable-jit \
    --enable-pcre2grep-jit \
%endif
    --disable-bsr-anycrlf \
    --disable-coverage \
    --disable-ebcdic \
    --disable-fuzz-support \
    --disable-never-backslash-C \
    --enable-newline-is-lf \
    --enable-pcre2-8 \
    --enable-pcre2-16 \
    --enable-pcre2-32 \
    --enable-unicode \
    --enable-pcre2grep-callout \
    --enable-pcre2grep-jit \
    --disable-pcre2grep-libbz2 \
    --disable-pcre2grep-libz \
    --disable-pcre2test-libedit \
    --enable-pcre2test-libreadline \
    --disable-rebuild-chartables \
    --enable-shared \
    --enable-stack-for-recursion \
    --enable-static \
    --enable-unicode \
    --disable-valgrind

%make

%install
%makeinstall_std
# These are handled by %%doc in %%files
rm -rf %{buildroot}%{_docdir}/pcre2

%check
%make check VERBOSE=yes
