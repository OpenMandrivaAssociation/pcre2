%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif

# Workaround for libtool being a broken mess if CC contains
# whitespace (as in "clang -target riscv64-openmandriva-linux-gnu",
# but not "riscv64-openmandriva-linux-gnu-gcc")
%if %{cross_compiling}
%define prefer_gcc 1
%endif

# -O3: matching is a hot path in many dependents
# -vp-counters-per-site: the interpreter has huge functions that overflow
# Clang's default PGO value-profile counters
%global optflags %{optflags} -O3
%if ! %{cross_compiling}
%global optflags %{optflags} -mllvm -vp-counters-per-site=64
%endif

%define major 3
%define umajor 0
%define oldposixlib %mklibname pcre2-posix 1
%define posixlib %mklibname pcre2-posix %{major}
%define posixlib32 libpcre2-posix%{major}
%define u8lib %mklibname pcre2-8 %{umajor}
%define u8lib32 libpcre2-8_%{umajor}
%define u16lib %mklibname pcre2-16 %{umajor}
%define u16lib32 libpcre2-16_%{umajor}
%define u32lib %mklibname pcre2-32 %{umajor}
%define u32lib32 libpcre2-32_%{umajor}
%define dev %mklibname -d pcre2
%define dev32 libpcre2-devel
%define static %mklibname -d -s pcre2

# Shared configure options (non-default only). --enable-jit=auto turns JIT
# on wherever sljit supports the CPU, including RISC-V.
# Must stay a single line so it is appended to %%configure / %%configure32.
%define pcre2_configure_opts --enable-jit=auto --enable-pcre2-16 --enable-pcre2-32

Name:		pcre2
Version:	10.48
Release:	4
%global		myversion %{version}%{?rcversion:-%rcversion}
Summary:	Perl-compatible regular expression library
Group:		System/Libraries
License:	BSD
URL:		https://www.pcre.org/
Source0:	https://github.com/PCRE2Project/pcre2/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	pkgconfig(readline)
# 32-bit compat + Clang PGO. clang -m32 / -target i686 reads
# i686-*.cfg (--sysroot /usr/i686-openmandriva-linux-gnu). compiler-rt.profile
# is in the cross clang package; CRT and headers are in cross libc; binutils
# ships the usr -> ./ symlink so lld can resolve the sysroot libc.so script;
# kernel-headers supply linux/limits.h (pulled in by glibc limits.h/pthread);
# atomic-devel ships both the 64-bit and 32-bit libatomic.so stubs. Gate on
# arch, not %%with compat32, so mock always installs them on x86_64/znver1.
%ifarch %{x86_64}
BuildRequires:	cross-i686-openmandriva-linux-gnu-clang
BuildRequires:	cross-i686-openmandriva-linux-gnu-gcc
BuildRequires:	cross-i686-openmandriva-linux-gnu-binutils
BuildRequires:	cross-i686-openmandriva-linux-gnu-libc
BuildRequires:	cross-i686-openmandriva-linux-gnu-kernel-headers
BuildRequires:	atomic-devel
%endif
%if %{with compat32}
BuildRequires:	libc6
%endif

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
%doc %{_mandir}/man1/pcre2grep.*
%doc %{_mandir}/man1/pcre2test.*

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
%doc %{_mandir}/man1/pcre2-config.*
%doc %{_mandir}/man3/*
%{_bindir}/pcre2-config
%doc doc/*.txt doc/html
%doc README HACKING ./src/pcre2demo.c

%package -n %{static}
Summary:	Static library for linking to PCRE2
Group:		Development/C
Provides:	%{name}-static-devel = %{EVRD}
Requires:	%{dev} = %{EVRD}

%description -n %{static}
Static library for linking to PCRE2.

%files -n %{static}
%{_libdir}/*.a

%if %{with compat32}
%package -n %{posixlib32}
Summary:	Version of the PCRE2 library providing a POSIX-like regex API (32-bit)
Group:		System/Libraries

%description -n %{posixlib32}
Version of the PCRE2 library providing a POSIX-like regex API. (32-bit)

%files -n %{posixlib32}
%{_prefix}/lib/libpcre2-posix.so.%{major}*

%package -n %{u8lib32}
Summary:	UTF-8 version of the PCRE2 library (32-bit)
Group:		System/Libraries

%description -n %{u8lib32}
UTF-8 version of the PCRE2 library. (32-bit)

%files -n %{u8lib32}
%{_prefix}/lib/libpcre2-8.so.%{umajor}*

%package -n %{u16lib32}
Summary:	UTF-16 version of the PCRE2 library (32-bit)
Group:		System/Libraries

%description -n %{u16lib32}
UTF-16 version of the PCRE2 library. (32-bit)

%files -n %{u16lib32}
%{_prefix}/lib/libpcre2-16.so.%{umajor}*

%package -n %{u32lib32}
Summary:	UTF-32 version of the PCRE2 library (32-bit)
Group:		System/Libraries

%description -n %{u32lib32}
UTF-32 version of the PCRE2 library. (32-bit)

%files -n %{u32lib32}
%{_prefix}/lib/libpcre2-32.so.%{umajor}*

%package -n %{dev32}
Summary:	Development files for the PCRE2 library (32-bit)
Group:		Development/C
Requires:	%{posixlib32} = %{EVRD}
Requires:	%{u8lib32} = %{EVRD}
Requires:	%{u16lib32} = %{EVRD}
Requires:	%{u32lib32} = %{EVRD}
Requires:	%{dev} = %{EVRD}

%description -n %{dev32}
Development files for the PCRE2 library. (32-bit)

%files -n %{dev32}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*
%endif

%prep
%autosetup -p1 -n %{name}-%{myversion}

%build
export CONFIGURE_TOP="$(pwd)"

# Use _OMV_rpm_build{,32} so the official %%pgo wipe keeps the sources.
%if %{with compat32}
# Subshell: %%configure32 exports CFLAGS and must not leak -target to 64-bit.
# cc -m32 looks for compiler-rt in i386-pc-linux-gnu; the profile runtime
# from cross-i686-...-clang lives under i686-openmandriva-linux-gnu.
(
	mkdir _OMV_rpm_build32
	cd _OMV_rpm_build32
	CFLAGS="${CFLAGS:-%{optflags}} -target i686-openmandriva-linux-gnu"
	CXXFLAGS="${CXXFLAGS:-%{optflags}} -target i686-openmandriva-linux-gnu"
	LDFLAGS="${LDFLAGS:-%{?build_ldflags}} -target i686-openmandriva-linux-gnu"
	export CFLAGS CXXFLAGS LDFLAGS
	%configure32 \
		%{pcre2_configure_opts}
	%make_build LIBTOOL=slibtool-shared
)
%endif

mkdir _OMV_rpm_build
cd _OMV_rpm_build
%configure \
	%{pcre2_configure_opts} \
	--enable-static \
	--enable-pcre2test-libreadline
%make_build LIBTOOL=slibtool
cd ..

# make check is a correctness suite (API corners, error diagnostics, limits)
# and would weight PGO toward rare paths. Train on grep-like scans of the
# source corpus and high-iteration matches of common patterns instead.
# Skipped automatically on cross-compile.
%pgo
pcre2_pgo_train() {
	local b="$1"
	local g="$b/pcre2grep"
	local t="$b/pcre2test"
	local in="$b/pgo-train.in"
	local p w
	[ -x "$g" ] && [ -x "$t" ] || return 0

	# File-scan path (JIT pcre2grep): identifiers, numbers, keywords,
	# includes, URLs, mail-ish, log tokens, whitespace.
	for p in \
		'[A-Za-z_][A-Za-z0-9_]*' \
		'[0-9]+' \
		'0x[0-9A-Fa-f]+' \
		'\b(if|while|for|return|static|const|struct)\b' \
		'^#\s*include' \
		'https?://[[:alnum:]./_~-]+' \
		'[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}' \
		'(error|warning|fail|FIXME|TODO)' \
		'.{0,40}pcre2' \
		'\s+'
	do
		"$g" -q -r --include='\.(c|h)$' -- "$p" src ||:
		"$g" -q -- "$p" testdata/grepinput ||:
	done
	"$g" -q -ri --include='\.(c|h)$' -- '\b[a-z]+\b' src ||:
	"$g" -q -u -r --include='\.(c|h|txt)$' -- '\w+' src doc ||:

	# Subjects must start with whitespace; do not put that indent in the
	# spec (rpmbuild strips leading whitespace from script lines).
	{
		echo '/^[A-Za-z_][A-Za-z0-9_]*$/'
		echo ' identifier'
		echo ' foo_bar123'
		echo ' Not an identifier!'
		echo '/\b\d{1,3}(\.\d{1,3}){3}\b/'
		echo ' host 10.0.0.1 ready'
		echo ' no address here'
		echo '/\b(error|warning|info|debug)\b/i'
		echo ' Error: disk full'
		echo ' this is a warning'
		echo ' nothing to see'
		echo '/https?:\/\/[[:alnum:].\/_~-]+/'
		echo ' see https://www.pcre.org/ for docs'
		echo ' no url'
		echo '/[A-Za-z0-9._+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/'
		echo ' mail bero@example.com please'
		echo ' not mail'
		echo '/^#\s*(define|include|ifdef)\b/'
		echo ' #include <stdio.h>'
		echo ' #define FOO 1'
		echo ' int x;'
	} > "$in"

	# Match hot path, all three widths: compile once, match many times.
	# testdata/testinput1 and testinput4 are the Perl-compatible matching
	# suites, not the error/API tests.
	for w in '' -16 -32; do
		"$t" $w -q -jit -tm 20000 "$in" /dev/null ||:
		"$t" $w -q -jit testdata/testinput1 /dev/null ||:
		"$t" $w -q -jit testdata/testinput4 /dev/null ||:
	done
}
%if %{with compat32}
pcre2_pgo_train _OMV_rpm_build32
%endif
pcre2_pgo_train _OMV_rpm_build

%install
%if %{with compat32}
%make_install -C _OMV_rpm_build32 LIBTOOL=slibtool-shared
%endif
%make_install -C _OMV_rpm_build LIBTOOL=slibtool
# These are handled by %%doc in %%files
rm -rf %{buildroot}%{_docdir}/pcre2

%if ! %{cross_compiling}
%check
%if %{with compat32}
make -C _OMV_rpm_build32 check VERBOSE=yes LIBTOOL=slibtool-shared
%endif
make -C _OMV_rpm_build check VERBOSE=yes LIBTOOL=slibtool
%endif
