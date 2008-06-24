#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
#
%define		_rel	6
Summary:	Intel(R) Wireless WiFi Link 4965AGN and Intel(R) PRO/Wireless 3945ABG Network Connection driver
Summary(en.UTF-8):	Intel® Wireless WiFi Link 4965AGN and Intel® PRO/Wireless 3945ABG Network Connection driver
Summary(pl.UTF-8):	Sterowniki do układów bezprzewodowych Intel® 4965AGN i 3945ABG
Name:		iwlwifi
Version:	1.2.25
Release:	%{_rel}
License:	mixed GPL v2 and BSD
Group:		Base/Kernel
Source0:	http://www.intellinuxwireless.org/iwlwifi/downloads/%{name}-%{version}.tgz
# Source0-md5:	e8726b20dd2f9457611019632709889a
Patch0:		%{name}-ieee80211_rate.patch
URL:		http://www.intellinuxwireless.org/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build > 3:2.6.22.10-4}
BuildRequires:	rpmbuild(macros) >= 1.379
#ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The iwlwifi project provides a driver which utilizes the new mac80211
subsystem for the Intel(R) Wireless WiFi Link 4965AGN and Intel(R)
PRO/Wireless 3945ABG Network Connection adapters.

In addition to using the new mac80211 subsystem, this project uses a
new microcode image which removes the need for the user space
regulatory daemon. This change should help to simplify installation,
development, and redistribution of this driver package.

%description -l en.UTF-8
The iwlwifi project provides a driver which utilizes the new mac80211
subsystem for the Intel® Wireless WiFi Link 4965AGN and Intel®
PRO/Wireless 3945ABG Network Connection adapters.

In addition to using the new mac80211 subsystem, this project uses a
new microcode image which removes the need for the user space
regulatory daemon. This change should help to simplify installation,
development, and redistribution of this driver package.

%description -l pl.UTF-8
Projekt iwlwifi udostępnia sterownik wykorzystujący nowy podsystem
mac80211, przeznaczony do układów bezprzewodowych Intel® Wireless WiFi
Link 4965AGN and Intel® PRO/Wireless 3945ABG Network Connection.

Oprócz używania nowego podsystemu mac80211 ten projekt wykorzystuje
nowy obraz mikrokodu eliminujący potrzebę używania demona regulującego
w przestrzeni użytkownika. Zmiana ta powinna ułatwić instalację,
rozwijanie i redystrybucję tego pakietu.

%package -n kernel%{_alt_kernel}-net-iwl3945
Summary:	Intel(R) PRO/Wireless 3945ABG Network Connection driver
Summary(en.UTF-8):	Intel® PRO/Wireless 3945ABG Network Connection driver
Summary(pl.UTF-8):	Sterownik do układów bezprzewodowych Intel® PRO/Wireless 3945ABG Network Connection
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kerqnel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	iwlwifi-3945-ucode
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-net-iwl3945
This package contains Linux kernel driver for the Intel(R)
PRO/Wireless 3945ABG Network Connection.

%description -n kernel%{_alt_kernel}-net-iwl3945 -l en.UTF-8
This package contains Linux kernel driver for the Intel® PRO/Wireless
3945ABG Network Connection.

%description -n kernel%{_alt_kernel}-net-iwl3945 -l pl.UTF-8
Ten pakiet zawiera sterownik jądra Linuksa do układów bezprzewodowych
Intel® PRO/Wireless 3945ABG Network Connection.

%package -n kernel%{_alt_kernel}-net-iwl4965
Summary:	Intel(R) Wireless WiFi Link 4965AG driver
Summary(en.UTF-8):	Intel® Wireless WiFi Link 4965AG driver
Summary(pl.UTF-8):	Sterownik do układów bezprzewodowych Intel® Wireless WiFi Link 4965AG
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel}
Requires(post,postun):	/sbin/depmod
Requires:	iwlwifi-4965-ucode
Requires:	module-init-tools >= 3.2.2-2

%description -n kernel%{_alt_kernel}-net-iwl4965
This package contains Linux kernel driver for the Intel(R) Wireless
WiFi Link 4965AGN.

%description -n kernel%{_alt_kernel}-net-iwl4965 -l en.UTF-8
This package contains Linux kernel driver for the Intel® Wireless WiFi
Link 4965AGN.

%description -n kernel%{_alt_kernel}-net-iwl4965 -l pl.UTF-8
Ten pakiet zawiera sterownik jądra Linuksa do układów bezprzewodowych
Intel® Wireless WiFi Link 4965AGN.

%prep
%setup -q
%patch0 -p1
sed -i -e 's#$(CONFIG_IWL3945)#m#g' -e 's#$(CONFIG_IWL4965)#m#g' origin/Makefile

%build
%build_kernel_modules -C origin -m iwl3945,iwl4965 

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m origin/iwl3945 -d kernel/drivers/net/wireless
%install_kernel_modules -m origin/iwl4965 -d kernel/drivers/net/wireless

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-net-iwl3945
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-iwl3945
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-net-iwl4965
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-net-iwl4965
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-net-iwl3945
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/iwl3945.ko*

%files -n kernel%{_alt_kernel}-net-iwl4965
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/iwl4965.ko*
