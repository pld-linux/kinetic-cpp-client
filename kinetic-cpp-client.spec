#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Kinetic C++ client library
Summary(pl.UTF-8):	Biblioteka kliencka C++ Kinetic
Name:		kinetic-cpp-client
Version:	0.1.1
Release:	4
License:	GPL v2+
Group:		Libraries
Source0:	https://github.com/Seagate/kinetic-cpp-client/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ac77cc4ebf388e0e1d690317888373e6
Patch0:		%{name}-system-libs.patch
URL:		https://github.com/Seagate/kinetic-cpp-client/
BuildRequires:	cmake >= 2.8.6
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	gflags-devel >= 2.0
BuildRequires:	glog-devel >= 0.3.3
BuildRequires:	gmock-devel >= 1.6.0
BuildRequires:	gtest-devel >= 1.6.0
BuildRequires:	kinetic-protocol >= 3.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	openssl-devel >= 1.0.1g
BuildRequires:	protobuf-devel >= 2.5.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains a library for producing Kinetic C++ clients for
interacting with Kinetic object-based storage.

%description -l pl.UTF-8
Ten pakiet zawiera bibliotekę do tworzenia w języku C++ klientów
Kinetic mających współpracować z opartym na obiektach systemem
przechowywania danych Kinetic.

%package devel
Summary:	Header files for Kinetic C++ client library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki klienckiej C++ Kinetic
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel
Requires:	openssl-devel
Requires:	protobuf-devel >= 2.5.0

%description devel
Header files for Kinetic C++ client library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki klienckiej C++ Kinetic.

%package apidocs
Summary:	Kinetic C++ client API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki klienckiej C++ Kinetic
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for Kinetic C++ client library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki klienckiej C++ Kinetic.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%{?with_apidocs:%{__make} doc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir}}

install build/libkinetic_client.so $RPM_BUILD_ROOT%{_libdir}
cp -pr include/kinetic $RPM_BUILD_ROOT%{_includedir}
cp -p src/main/generated/kinetic_client.pb.h $RPM_BUILD_ROOT%{_includedir}/kinetic

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libkinetic_client.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/kinetic

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/*.{css,html,js,png}
%endif
