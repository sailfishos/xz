Name:       xz
Summary:    LZMA compression utilities
Version:    5.2.5
Release:    1
License:    GPLv2+ and Public Domain
URL:        https://tukaani.org/xz/
Source0:    %{name}-%{version}.tar.bz2
Requires:   %{name}-libs = %{version}-%{release}

BuildRequires: automake
BuildRequires: libtool
BuildRequires: gettext-devel

%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package libs
Summary:    Libraries for decoding LZMA compression
License:    Public Domain
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package lzma-compat
Summary:    Older LZMA format compatibility binaries
License:    Public Domain
Requires:   %{name} = %{version}-%{release}
Provides:   lzma = 5
Obsoletes:  lzma < 5

%description lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.


%package devel
Summary:    Devel libraries & headers for liblzma
License:    Public Domain
Requires:   %{name}-libs = %{version}-%{release}

%description devel
Devel libraries and headers for liblzma.


%package doc
Summary:    Documentation for %{name}
BuildArch:  noarch
Requires:   %{name} = %{version}-%{release}
Obsoletes:  %{name}-docs

%description doc
Man pages and other documentation for %{name}.


%prep
%autosetup -n %{name}-%{version}/upstream

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS ;
CXXFLAGS="${CXXFLAGS:-%optflags}" ; export CXXFLAGS ;
FFLAGS="${FFLAGS:-%optflags -I%_fmoddir}" ; export FFLAGS ;
autoreconf -v --install --force || exit 1
%configure --disable-static --disable-nls
%make_build

%install
%make_install

%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING*
%{_bindir}/*xz*

%files libs
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/lib*.so.*

%files lzma-compat
%defattr(-,root,root,-)
%{_bindir}/*lz*

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/lzma
%{_includedir}/lzma/*.h
%{_includedir}/lzma.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/liblzma.pc

%files doc
%defattr(-,root,root,-)
%{_docdir}/%{name}/
%{_mandir}/man1/
