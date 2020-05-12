%define major 2
%define umajor 0
%define oldposixlib %mklibname pcre2-posix 1
%define posixlib %mklibname pcre2-posix %{major}
%define u8lib %mklibname pcre2-8 %{umajor}
%define u16lib %mklibname pcre2-16 %{umajor}
%define u32lib %mklibname pcre2-32 %{umajor}
%define dev %mklibname -d pcre2
%define static %mklibname -d -s pcre2

%bcond_without pgo

# (tpg) optimize a bit
%global optflags %{optflags} -O3

Name:		pcre2
Version:	10.35
Release:	1
%global		myversion %{version}%{?rcversion:-%rcversion}
Summary:	Perl-compatible regular expression library
Group:		System/Libraries
License:	BSD
URL:		http://www.pcre.org/
Source0:	https://ftp.pcre.org/pub/pcre/%{name}-%{version}.zip
# Do no set RPATH if libdir is not /usr/lib
Patch0:		pcre2-10.10-Fix-multilib.patch
BuildRequires:	pkgconfig(readline)
BuildRequires:	pkgconfig(bzip2)
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
%autosetup -p1 -n %{name}-%{myversion}

# Because of multilib patch
libtoolize --copy --force
autoreconf -vif

%build
%if %{with pgo}
CFLAGS="%{optflags} -fprofile-instr-generate" \
CXXFLAGS="%{optflags} -fprofile-instr-generate" \
LDFLAGS="%{ldflags} -fprofile-instr-generate" \
%configure \
%ifarch riscv64
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
    --enable-percent-zt \
    --enable-shared \
    --enable-stack-for-recursion \
    --disable-static \
    --enable-unicode \
    --disable-valgrind

%make_build

make check VERBOSE=yes

unset LD_LIBRARY_PATH
unset LLVM_PROFILE_FILE
llvm-profdata merge --output=%{name}.profile $(find . -type f -name "*.profile.d")
rm -f *.profile.d

make clean

CFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
CXXFLAGS="%{optflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
LDFLAGS="%{ldflags} -fprofile-instr-use=$(realpath %{name}.profile)" \
%endif
%configure \
%ifarch riscv64
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
    --enable-percent-zt \
    --enable-shared \
    --enable-stack-for-recursion \
    --enable-static \
    --enable-unicode \
    --disable-valgrind

%make_build

%install
%make_install
# These are handled by %%doc in %%files
rm -rf %{buildroot}%{_docdir}/pcre2

%check
make check VERBOSE=yes
