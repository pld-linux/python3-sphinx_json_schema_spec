#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

Summary:	Sphinx support for the JSON Schema specifications
Summary(pl.UTF-8):	Wsparcie Sphinksa dla specyfikacji JSON Schema
Name:		python3-sphinx_json_schema_spec
Version:	2025.1.1
Release:	1
License:	MIT (plugin), BSD/AFL v1.0 (schema)
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/sphinx-json-schema-spec/
Source0:	https://files.pythonhosted.org/packages/source/s/sphinx-json-schema-spec/sphinx_json_schema_spec-%{version}.tar.gz
# Source0-md5:	b6202a9e464b2f1258927792c81d4abc
Source1:	https://json-schema.org/draft/2020-12/json-schema-core.html
# Source1-md5:	c05a695bb4a7b9db39e0692e1e36af41
Source2:	https://json-schema.org/draft/2020-12/json-schema-validation.html
# Source2-md5:	3a5ec7f1a6bc956fb2d2a04956bd07f2
Source3:	https://json-schema.org/learn/glossary.html
# Source3-md5:	1ea137b5836ab9f60ed0f62578d4f754
Patch0:		sphinx_json_schema_spec-offline.patch
URL:		https://pypi.org/project/sphinx-json-schema-spec/
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.11
%if %{with tests}
BuildRequires:	python3-Sphinx >= 5.1.1
BuildRequires:	python3-lxml
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinxcontrib-spelling > 5
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3 >= 5.1
%endif
Requires:	python3-modules >= 1:3.11
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Sphinx extension providing a role which allows linking to sections
within the JSON Schema specifications (<https://json-schema.org/>).

It is intended for use by implementations of JSON Schema (in Python or
otherwise) who may wish to interlink to the specification in their own
documentation.

%description -l pl.UTF-8
Rozszerzenie Sphinksa udostępniające rolę pozwalającą łączenie do
sekcji w specyfikacjach JSON Schema (<https://json-schema.org/>).

Jest przeznaczone do użycia w implementacjach JSON Schema (w Pythonie
i nie tylko), chcących dodać powiązania do specyfikacji we własnej
dokumentacji.

%package apidocs
Summary:	API documentation for Python sphinx_json_schema_spec module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona sphinx_json_schema_spec
Group:		Documentation

%description apidocs
API documentation for Python sphinx_json_schema_spec module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona sphinx_json_schema_spec.

%prep
%setup -q -n sphinx_json_schema_spec-%{version}
%patch -P0 -p1

install -d _cache
cp -p %{SOURCE1} _cache/core.html
cp -p %{SOURCE2} _cache/validation.html
cp -p %{SOURCE3} _cache/glossary.html

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest sphinx_json_schema_spec/tests
%endif

%if %{with doc}
# metadata is needed
%{__python3} -m zipfile -e build-3/*.whl build-3-doc

PYTHONPATH=$(pwd)/build-3-doc \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3 \
	SPHINXOPTS="-Dcache_path=$(pwd)/_cache"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_json_schema_spec/_cache
cp -p _cache/*.html $RPM_BUILD_ROOT%{py3_sitescriptdir}/sphinx_json_schema_spec/_cache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README.rst
%{py3_sitescriptdir}/sphinx_json_schema_spec
%{py3_sitescriptdir}/sphinx_json_schema_spec-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
