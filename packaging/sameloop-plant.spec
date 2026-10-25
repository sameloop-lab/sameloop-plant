Name:           sameloop-plant
Version:        0.1.0
Release:        1%{?dist}
Summary:        SameLoop deterministic thermal simulator
License:        MIT
Source0:        sameloop_plant-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(setuptools) >= 77
BuildRequires:  python3dist(wheel)

%description
SameLoop deterministic thermal simulator.
Initial Linux demonstration profile; no hardware or AGL image integration.

%prep
%autosetup -n sameloop_plant-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files sameloop_plant

%check
PYTHONPATH=src %{__python3} -m unittest discover -s tests -p 'test_*.py' -v

%files -f %{pyproject_files}
%license LICENSE
%doc README.md docs
%{_bindir}/sameloop-plant

%changelog
* Sun Oct 25 2026 SameLoop contributors - 0.1.0-1
- Initial packaging draft; mock/OBS validation pending.
