Name:       xz
Summary:    LZMA compression utilities
Version:    5.0.4
Release:    2
Group:      Applications/File
License:    LGPLv2+
URL:        http://tukaani.org/%{name}/
Source0:    http://tukaani.org/%{name}/xz-%{version}.tar.bz2
Requires:   %{name}-libs = %{version}-%{release}

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
License:    LGPLv2+
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package lzma-compat
Summary:    Older LZMA format compatibility binaries
License:    GPLv2+ and LGPLv2+
Group:      System/Libraries
Requires:   %{name} = %{version}-%{release}
Provides:   lzma = 5
Obsoletes:  lzma < 5

%description lzma-compat
The lzma-compat package contains compatibility links for older
commands that deal with the older LZMA format.


%package devel
Summary:    Devel libraries & headers for liblzma
License:    LGPLv2+
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   %{name}-libs = %{version}-%{release}

%description devel
Devel libraries and headers for liblzma.


%package doc
Summary:    Documentation for %{name}
Group:      Documentation
Requires:   %{name} = %{version}-%{release}
Obsoletes:  %{name}-docs

%description doc
Man pages and other documentation for %{name}.


%prep
%setup -q -n %{name}-%{version}


%build
CFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64" \
%configure --disable-static \
--disable-nls

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool


make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install

mv %{buildroot}/%{_docdir}/%{name} %{buildroot}/%{_docdir}/%{name}-%{version}
rm %{buildroot}/%{_docdir}/%{name}-%{version}/COPYING*


%check
LD_LIBRARY_PATH=$PWD/src/liblzma/.libs make check

%post libs -p /sbin/ldconfig

%postun libs
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.*
%{_bindir}/*xz*

%files libs
%defattr(-,root,root,-)
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
%doc %{_docdir}/%{name}-%{version}
%{_mandir}/man*/*
