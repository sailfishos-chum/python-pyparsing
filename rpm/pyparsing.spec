# Adapted https://src.fedoraproject.org/rpms/pyparsing/blob/rawhide/f/pyparsing.spec for SailfishOS
# TODO build wheel (missing dependency python-wheel, creates dependency loop packaging <-> pyparsing)
%global dist_name pyparsing
# suffix of python executable
%global python_pkgversion 3

%define source_date_epoch_from_changelog 1
%define clamp_mtime_to_source_date_epoch 1
%define use_source_date_epoch_as_buildtime 1

Name:           python3-pyparsing
Summary:        Library for creating PEG (parsing expression grammar) parsers
Version:        2.4.7
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/pyparsing/pyparsing
Source:         %{name}-%{version}.tar.bz2
BuildArch:      noarch
BuildRequires:  python%{python_pkgversion}-devel
BuildRequires:  python%{python_pkgversion}-setuptools

# disable bootstrap by default
%bcond_with bootstrap
%if %{with bootstrap}
%bcond_with docs
%else
%bcond_without docs
%endif
%if %{with docs}
BuildRequires:  python3-sphinx
%endif

%description
The pyparsing module is an alternative approach to creating and executing 
simple grammars, vs. the traditional lex/yacc approach, or the use of regular
expressions. The pyparsing module provides a library of classes that client
code uses to construct the grammar directly in Python code.

%if %{with docs}
%package -n python-%{dist_name}-doc
Summary:        Documentation for %{name}

%description -n python-%{dist_name}-doc
This package contains documentation for %{dist_name}.
%endif

%prep
%autosetup -n %{name}-%{version}/pyparsing

%build
%py3_build

%if %{with docs}
# Theme not available
sed -i '/alabaster/d' docs/conf.py
sphinx-build -b html docs docs/html
# cleanup
rm -rf docs/html/.{doctrees,buildinfo}
%endif

%install
%py3_install
# cleanup
rm %{buildroot}/%{python3_sitelib}/%{dist_name}-*.egg-info/SOURCES.txt

%check
%{__python3} unitTests.py
%{__python3} simple_unit_tests.py

%files
%license LICENSE
%doc CHANGES README.rst
%{python3_sitelib}/pyparsing.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/pyparsing-*-info/

%if %{with docs}
%files -n python-%{dist_name}-doc
%license LICENSE
%doc CHANGES README.rst docs/html examples
%endif

%changelog
* Fri Feb 04 2022 takimata <takimata@gmx.de> - 2.4.7-1
- Initial packaging for Chum
